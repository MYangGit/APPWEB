import dill
import json
from pathlib import Path
import numpy as np
import matplotlib
import sys
try:
    import tornado
except ImportError as err:
    raise RuntimeError("This example requires tornado.") from err
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import base64
from matplotlib._pylab_helpers import Gcf

import matplotlib as mpl
from matplotlib.backends.backend_webagg import (
    FigureManagerWebAgg, new_figure_manager_given_figure,ipython_inline_display)

import numpy as np
import os

i = 0

def get_home_dir():
    '''
    获得当前用户家目录，支持windows，linux和macosx
    更新方法，更加简单
    :return:
    '''        
    # if "USER_DATA_DIR" in os.environ:
    #     homedir = os.environ["USER_DATA_DIR"]
    # else:
    homedir = str(Path.home())
        
    return homedir

def get_fig_dir():
    userHome = get_home_dir()
    fig_dir = f"{userHome}/SyslabCloud/figure_dir"

    setting_path = f"{userHome}/SyslabCloud/.syslab-oss/syslab-config.json"
    if os.path.exists(setting_path):
        with open(setting_path) as f:
            content = f.read()
            json_data = json.loads(content)
            if "user-fig-path" in json_data:
                fig_dir = os.path.join(json_data["user-fig-path"],"figure_dir")
    
    return fig_dir

def create_figure(figId,figPklPath:False):
    """
    Creates a simple example figure.
    """
    matplotlib.use('WebAgg')
    matplotlib.rcParams['agg.path.chunksize'] = 10000
    matplotlib.rcParams['path.simplify_threshold'] = 1
    # 获取当前用户的主目录
    
    fig_dir = get_fig_dir()

    serializedPath = r"{0}/{1}.pkl".format(fig_dir,figId)
    if figPklPath:
        serializedPath = figPklPath
    if not os.path.exists(serializedPath):
        return None
    print(serializedPath)

    # 兼容旧版本的RadialTick类和MwThetaFormatter类的位置
    import TyPlotOnline.utility.mw_plotting_utils as mw_plotting_utils
    sys.modules['objects.mw_interface'] = mw_plotting_utils

    sys.path.append(os.path.dirname(TyPlotOnline.__file__))
    with open(serializedPath, "rb") as f:
        serialized_fig = f.read()
        # fig = dill.loads(serialized_fig)
        fig = syslab_loads(serialized_fig)
        print(fig.__class__.__name__)


    try:
        if figPklPath == False:
            os.remove(serializedPath)
    except:
        pass

    if fig.__class__.__name__ == "CFigure":
        figid = id(fig.fig)
    else:
        figid = id(fig)

    print('create figure, figid is ',figid)
    return fig

import TyPlotOnline
from TyPlotOnline.mw_main import init
from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.objects.mw_figure import mw_update_clines,mw_update_scatters,mw_update_caxe
from TyPlotOnline.mw_actions import *
from TyPlotOnline.mw_prop import mw_set_prop, mw_close_webserver, mw_delete_current_datatip, mw_delete_all_datatips, mw_property_init, mw_change_select_objs, mw_property_close,mw_property_ready
from TyPlotOnline.objects.mw_axes_yyaxis import CAxesYyaxis
from mpl_toolkits.mplot3d.art3d import Line3D, Path3DCollection

def init_figures(fig,figId, is_import=False):
    init(fig, init = False, is_import = is_import)

    fig.setting=None

    fignum = id(fig)
    # fignum = fig.number
    manager = new_figure_manager_given_figure(fignum, fig)
    fig.canvas.handle_set_prop = mw_set_prop
    fig.canvas.handle_delete_current_datatip = mw_delete_current_datatip
    fig.canvas.handle_delete_all_datatips = mw_delete_all_datatips
    fig.canvas.handle_property_init = mw_property_init
    fig.canvas.handle_property_ready = mw_property_ready
    fig.canvas.handle_change_select_objs = mw_change_select_objs
    fig.canvas.handle_property_close = mw_property_close
    
    manager.toolbar.editmode = action_editmode
    manager.toolbar.grid = action_grid
    manager.toolbar.legend = action_legend
    manager.toolbar.cursor = action_cursor
    manager.toolbar.ty_pan = action_pan
    manager.toolbar.ty_zoom = action_zoom
    manager.toolbar.home = action_home
    manager.toolbar.data_tips = action_datatips
    manager.toolbar.draw_text = action_darw_text
    manager.toolbar.draw_rect = action_draw_rect
    manager.toolbar.draw_ellipse = action_draw_ellipse
    manager.toolbar.draw_line = action_draw_line
    manager.toolbar.draw_arrow = action_draw_arrow
    manager.toolbar.draw_text_arrow = action_draw_textarrow
    manager.toolbar.draw_double_arrow = action_draw_doublearrow

    # ws_url="ws://localhost:8080/{figId}/ws".format(figId=figId)
    # os.chdir(os.path.dirname(__file__))
    # userHome = os.environ['USERPROFILE']
    # with open('{0}/syslab/webagg0.html'.format(userHome,figId), 'r+',encoding='utf-8') as file:
    #     data=re.sub(r'ws://localhost:8080/\d+/ws', ws_url, file.read())
    # with open('{0}/syslab/{1}.html'.format(userHome,figId), 'w',encoding='utf-8') as file:
    #     file.write(data)
    #     file.close()
    # print("figId",figId,ws_url)
    # if not figId in APPLICATION.figures:
    #     APPLICATION.figures[figId]=dict()
    # APPLICATION.figures[figId]['fig']=fig
    # APPLICATION.figures[figId]['manager']=manager
    return manager

import dill
from io import BytesIO as StringIO

class SyslabUnpickler(dill.Unpickler):
    def find_class(self, module, name):
        try:
            if name == "Proj":
                raise Exception("geomap")
            return super(SyslabUnpickler, self).find_class(module, name)
        except (AttributeError, ModuleNotFoundError):
            print(module)
            print(name)
            print("not found")
            return CNotFound

    # def load(self): #NOTE: if settings change, need to update attributes
    #     obj = super(SyslabUnpickler, self).load()
    #     print(type(obj))
    #     return obj

def syslab_load(file, ignore=None, **kwds):
    try:
        cfig = SyslabUnpickler(file, ignore=ignore, **kwds).load()
    except Exception as e:
        if e.__str__() == "geomap":
            raise Exception("geomap")
        else:
            cfig = None
    return cfig

def syslab_loads(str, ignore=True,**kwds):
    file = StringIO(str)
    return syslab_load(file, ignore, **kwds)

# The following is the content of the web page.  You would normally
# generate this using some sort of template facility in your web
# framework, but here we just use Python string formatting.

class MyApplication(tornado.web.Application):
    print("MyApplication", tornado.web.Application)
    """Plotting application"""
    figures = dict()
    index=1
    ws_connections = dict()

    # png_base64 = dict()

    class MplJs(tornado.web.RequestHandler):
        """
        Serves the generated matplotlib javascript file.  The content
        is dynamically generated based on which toolbar functions the
        user has defined.  Call `FigureManagerWebAgg` to get its
        content.
        """
        def get(self):
            self.set_header('Content-Type', 'application/javascript')
            js_content = FigureManagerWebAgg.get_javascript()
            with open('static/mpl.js', 'r',encoding='utf-8') as fh:
                local_content = fh.read()
            self.write(local_content)

    class Download(tornado.web.RequestHandler):
        """
        Handles downloading of the figure in various file formats.
        """
        def post(self):
            json_data = json.loads(self.request.body)
            figId = json_data.get('figId')
            figId = int(figId)
            filename = json_data.get('filename')
            fmt = json_data.get('fmt')

            if figId in self.application.figures:
                manager = self.application.figures[figId]["manager"]
            else:
                self.write({"status": False, "message": "can't find manager."})
                return

            mimetypes = {
                'ps': 'application/postscript',
                'eps': 'application/postscript',
                'pdf': 'application/pdf',
                'svg': 'image/svg+xml',
                'png': 'image/png',
                'jpeg': 'image/jpeg',
                'tif': 'image/tiff'
            }

            self.set_header('Content-Type', mimetypes.get(fmt, 'binary'))

            # buff = io.BytesIO()
            # manager.canvas.print_figure(buff, format=fmt)
            try:
                manager.canvas.print_figure(filename, format=fmt)
                self.write({"status": True, "message": ""})
            except Exception as e:
                self.write({"status": False, "message": e})
            # self.write(buff.getvalue())

    class ExportCSV(tornado.web.RequestHandler):
        def post(self):
            json_data = json.loads(self.request.body)
            figId = json_data.get('figId')
            figId = int(figId)
            filename = json_data.get('filename')

            if figId in self.application.figures:
                figure = self.application.figures[figId]["fig"]
                lines = figure.gca().get_lines()
                lst = []

                for line in lines:
                    x_data = line.get_xdata()
                    y_data = line.get_ydata()

                    lst.append(x_data)
                    lst.append(y_data)

                new_lst = list(map(list,zip(*lst)))
                try:
                    np.savetxt(filename, new_lst, delimiter=',')
                    self.write({"status": True, "message": "Export CSV successed."})
                except Exception as e:
                    self.write({"status": False, "message": e})
            else:
                self.write({"status": False, "message": f"{figId} not found."})
                    
        
    class WebSocket(tornado.websocket.WebSocketHandler):
        """
        A websocket for interactive communication between the plot in
        the browser and the server.

        In addition to the methods required by tornado, it is required to
        have two callback methods:

            - ``send_json(json_content)`` is called by matplotlib when
              it needs to send json to the browser.  `json_content` is
              a JSON tree (Python dictionary), and it is the responsibility
              of this implementation to encode it as a string to send over
              the socket.

            - ``send_binary(blob)`` is called to send binary image data
              to the browser.
        """
        supports_binary = True
        def check_origin(self, origin):
            return True
        
        def open(self, fignum):
            self.fignum = int(fignum)
            print("webscket open:", self.fignum)

            # Register the websocket with the FigureManager.
            if self.fignum in self.application.figures:
                manager = self.application.figures[self.fignum]['manager']
                fig = self.application.figures[self.fignum]['fig']
                manager.add_web_socket(self)
                # manager.num = fig.number
                Gcf.set_active(manager)

                fig = self.application.figures[self.fignum]['fig']
                # 获取当前CFigure对象
                cfig = mw_get_cfig(fig)
                # 获取当前CFigure的所有CAxes对象
                axes = cfig.axs
                if len(axes) > 0:
                    for ax in axes:
                        # 更新每一个CAxes对应的grid与legend状态
                        ax.init_toolbar_status()

                if hasattr(self, 'set_nodelay'):
                    self.set_nodelay(True)
            else:
                self.send_json({'type':'close'})

        def on_close(self):
            # When the socket is closed, deregister the websocket with
            # the FigureManager.
            # 通信断开删除figure
            # fig, manager = self.application.figures.pop(self.fignum)
            # fig = self.application.figures[self.fignum]['fig']
            print("webscket close:", self.fignum)
            
            if self.fignum in self.application.figures:
                manager = self.application.figures[self.fignum]['manager']
                if self in manager.web_sockets:
                    manager.remove_web_socket(self)


        def on_message(self, message):
            # Every message has a "type" and a "figure_id".
            message = json.loads(message)
            # if not message['type'] == 'motion_notify':
            #     print(message)
            if message['type'] == 'supports_binary':
                self.supports_binary = message['value']
            elif message['type'] == 'ping':  
                # self.send_json({'type':'pong'})
                self.send_json('pong')
            elif message['type'] == 'heartbeat':
                pass
            elif self.fignum in self.application.figures:
                manager = self.application.figures[self.fignum]['manager']
                manager.handle_json(message)


        def send_json(self, content):
            self.write_message(json.dumps(content))

        def send_binary(self, blob):
            if self.supports_binary:
                # print '-' * 80
                # print 'send binary image data to the browser'
                # print '-' * 80
                data_uri = ("data:image/png;base64," +base64.b64encode(blob).decode("utf-8"))
                self.write_message(data_uri)
                # self.write_message(blob, binary=True)
            else:
                data_uri = ("data:image/png;base64," +base64.b64encode(blob).decode("utf-8"))
                self.write_message(data_uri)
    class AttributeWebSocket(tornado.websocket.WebSocketHandler):
        """
        A websocket for interactive communication between the plot in
        the browser and the server.

        In addition to the methods required by tornado, it is required to
        have two callback methods:

            - ``send_json(json_content)`` is called by matplotlib when
              it needs to send json to the browser.  `json_content` is
              a JSON tree (Python dictionary), and it is the responsibility
              of this implementation to encode it as a string to send over
              the socket.

            - ``send_binary(blob)`` is called to send binary image data
              to the browser.
        """
        supports_binary = True
        def check_origin(self, origin):
            return True
        
        def open(self, fignum):
            self.fignum = int(fignum)
            print("AttributeWebSocket open:", self.fignum)

            # Register the websocket with the FigureManager.
            if self.fignum in self.application.figures:
                manager = self.application.figures[self.fignum]['manager']
                # fig = self.application.figures[self.fignum]['fig']
                manager.add_web_attribute_socket(self)
                # manager.num = fig.number
                # Gcf.set_active(manager)

                # fig = self.application.figures[self.fignum]['fig']
                # # 获取当前CFigure对象
                # cfig = mw_get_cfig(fig)
                # # 获取当前CFigure的所有CAxes对象
                # axes = cfig.axs
                # if len(axes) > 0:
                #     for ax in axes:
                #         # 更新每一个CAxes对应的grid与legend状态
                #         ax.init_toolbar_status()

                # if hasattr(self, 'set_nodelay'):
                #     self.set_nodelay(True)
            else:
                self.send_json({'type':'close'})

        def on_close(self):
            # When the socket is closed, deregister the websocket with
            # the FigureManager.
            # 通信断开删除figure
            # fig, manager = self.application.figures.pop(self.fignum)
            # fig = self.application.figures[self.fignum]['fig']
            print("webscket close:", self.fignum)
            
            if self.fignum in self.application.figures:
                manager = self.application.figures[self.fignum]['manager']
                if self in manager.web_sockets:
                    manager.remove_web_socket(self)


        def on_message(self, message):
            # Every message has a "type" and a "figure_id".
            message = json.loads(message)
            # if not message['type'] == 'motion_notify':
            #     print(message)
            if message['type'] == 'supports_binary':
                self.supports_binary = message['value']
            elif message['type'] == 'ping':  
                # self.send_json({'type':'pong'})
                self.send_json('pong')
            elif message['type'] == 'heartbeat':
                pass
            elif self.fignum in self.application.figures:
                manager = self.application.figures[self.fignum]['manager']
                manager.handle_json(message)


        def send_json(self, content):
            self.write_message(json.dumps(content))

        def send_binary(self, blob):
            if self.supports_binary:
                # print '-' * 80
                # print 'send binary image data to the browser'
                # print '-' * 80
                data_uri = ("data:image/png;base64," +base64.b64encode(blob).decode("utf-8"))
                self.write_message(data_uri)
                # self.write_message(blob, binary=True)
            else:
                data_uri = ("data:image/png;base64," +base64.b64encode(blob).decode("utf-8"))
                self.write_message(data_uri)

    # class WebSocketInner(tornado.websocket.WebSocketHandler):
    #     supports_binary = True
    #     def check_origin(self, origin):
    #       return True
        
    #     def open(self, figId):
    #         figId = int(figId)
    #         self.application.ws_connections[figId] = self
    #         # print("open: " + figId)

    #     def on_close(self):
    #         for k in list(self.application.ws_connections):
    #             if self.application.ws_connections[k] == self:
    #                 self.application.ws_connections.pop(k)
    #         print("close")

    #     def on_message(self, message):
    #         print("message: ", message)

    class InitFigureHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

        def get(self):
            # figId = self.get_argument('figId')
            # figId = int(figId)
            # ws = self.application.ws_connections[figId]

            figId = self.get_argument('figId')
            figId = int(figId)
            figPklPath = self.get_argument('figPklPath',False)
            fig = None
            cfig = None
            try:
                create_fig = create_figure(figId,figPklPath)
                if create_fig.__class__.__name__ == "CFigure":
                    fig = create_fig.fig
                    cfig = create_fig
                    cfig.after_import()
                    CGlobalSetting.c_fig_lst.append(cfig)
                    for cax in cfig.axs:
                        cax.after_import()
                else:
                    fig = create_fig
            except Exception as e:
                self.write({"status": False, "message": e})
                return

                
            # if fig == None:
            #     self.write({"status": False, "message": "Init figure failed"})
            #     return
            
            # print(self.application.figures)
            if fig == None:
                if figId in self.application.figures and 'fig' in self.application.figures[figId]:
                    fig = self.application.figures[figId]['fig']
                else:
                    self.write({"status": False, "message": "Init figure failed"})
                    return

            if figId not in self.application.figures:
                self.application.figures[figId]=dict()
            
            if cfig == None:
                cfig = mw_get_cfig(fig)
                
            is_import = True if cfig != None else False
            manager = init_figures(fig,figId, is_import=is_import)
            self.application.figures[figId]['fig']=fig
            self.application.figures[figId]['manager']=manager

            print("init successed")
            self.write({"status": True, "message": "success"})

    class InteractiveHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

        def get(self):
            print("打开交互模式")
            # self.application.ws


    class initWebaggFigureHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

        def get(self):
            figId = self.get_argument('figId')
            print('初始化webagg_figure',figId)

    class SavePngBase64Handler(tornado.web.RequestHandler):
        def post(self):
            fig_id = self.get_body_argument('figId')
            fig_id = int(fig_id)

            png_base64 = self.get_body_argument('png')
            if not fig_id in self.application.figures:
                self.application.figures[fig_id]=dict() 
            self.application.figures[fig_id]['png_base64'] = png_base64
            print("save base64")
            self.write({"status": True, "message": f"figure {fig_id} base64 save successed"})

            # userHome = os.environ['USERPROFILE']
            # # userId = os.environ['SYSLAB_ONLINE_USERID']
            # json_path = r"{0}/Syslab/fig.json".format(userHome)

            # print(json_path)
            # data = {"figId": fig_id, "webServer": True}
            # with open(json_path, "w") as f:
            #     json.dump(data, f)
            # self.write("创建json文件")

    class SetActiveFigureHandler(tornado.web.RequestHandler):
        def get(self):
            fig_id = self.get_argument('figId')
            print("fig_id==",fig_id)
            fig_id = int(fig_id)
            # print("self.application.figures===",self.application.figures)
            if fig_id in self.application.figures and 'manager' in self.application.figures[fig_id]:
                manager = self.application.figures[fig_id]['manager']
                # manager.num = fig.number
                Gcf.set_active(manager)
            self.write({"status": True, "message": f"figure {fig_id} setActive"})

    class GetPngBase64Handler(tornado.web.RequestHandler):
        def set_default_headers(self):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        def get(self):
            fig_id = self.get_argument('figId')
            fig_id = int(fig_id)

            png_base64 = None
            try:
                png_base64 = self.application.figures[fig_id]['png_base64']
                # print(png_base64)
            except Exception as e:
                self.write({"status": False, "value": png_base64, "message": e})
                return 

            self.write({"status": True, "value": str(png_base64), "message": "Get png base64 successed."})

    class RemoveWebaggFigureHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

        def get(self):
            figId = self.get_argument('figId')
            figId = int(figId)
            if figId in self.application.figures:
                if 'fig' in self.application.figures[figId]:
                    print(self.application.figures[figId]['fig'].number)
                    plt.close(self.application.figures[figId]['fig'].number)
                self.application.figures.pop(figId)
            print(plt.get_fignums())

            fig_dir = get_fig_dir()
            serializedPath = r"{0}/{1}.pkl".format(fig_dir,figId)
            if os.path.exists(serializedPath):
                try:
                    os.remove(serializedPath)
                except:
                    pass
            
            print('删除 webagg_figure', figId)

    class UpdateFigureHandler(tornado.web.RequestHandler):
        def set_default_headers(self):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

        def get(self):
            figId = self.get_argument('figId')
            figId = int(figId)
            figPklPath = self.get_argument('figPklPath',False)
            fig = None
            try:
                fig = create_figure(figId,figPklPath)
            except Exception as e:
                self.write({"status": False, "message": e})
                return

            if fig == None:
                self.write({"status": True, "message": "已更新到最新"})
                return
            
            if figId not in self.application.figures:
                self.application.figures[figId]=dict()
            elif 'manager' in self.application.figures[figId]:
                for ws in self.application.figures[figId]['manager'].web_sockets:
                    ws.send_json({"type": "reconnect"})
                    # ws.close()

            manager = None
            try:
                manager = init_figures(fig, figId)
            except Exception as e:
                self.write({"status": False, "message": e})
                return

            self.application.figures[figId]['fig']=fig
            self.application.figures[figId]['manager']=manager

            print("update figure successed")
            self.write({"status": True, "message": "Update figure success"})

            print('update webagg_figure',figId)

    class FileExists(tornado.web.RequestHandler):
        def set_default_headers(self):
            self.set_header('Access-Control-Allow-Origin', '*')
            self.set_header('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

        def get(self):
            figId = self.get_argument('figId')
            figId = int(figId)
            figPklPath = self.get_argument('figPklPath',False)
            fig_dir = get_fig_dir()

            serializedPath = r"{0}/{1}.pkl".format(fig_dir,figId)
            if figPklPath:
                serializedPath = figPklPath
            # self.write({"status": True, "message": "file is exists"})
            if figId in self.application.figures and 'fig' in self.application.figures[figId]:
                self.write({"status": True, "message": "file is exists"})
                return

            if not os.path.exists(serializedPath):
                self.write({"status": False, "message": f"file is not exists:{serializedPath}"})
            else:
                self.write({"status": True, "message": "file is exists"})
    
    class ExportFigure(tornado.web.RequestHandler):
        def post(self):
            json_data = json.loads(self.request.body)
            figId = json_data.get('figId')
            figId = int(figId)
            filename = json_data.get('filename')
            print("figId: ", figId)
            print("filename: ", filename)

            if figId in self.application.figures and "fig" in self.application.figures[figId]:
                # try:
                fig = self.application.figures[figId]["fig"]
                self.export_fig(fig, filename)
                self.write({"status": True, "message": "export figure successed."})
                # except:
                #     self.write({"status": False, "message": "export figure failed."})
            else:
                self.write({"status": False, "message": "figure not found."})

        def export_fig(self, fig, filename):
            import time
            a = time.time()
            print("save fig")
            cfig = mw_get_cfig(fig)
            cfig.before_export()

            serialized_fig = dill.dumps(cfig)
            with open(filename, "wb") as f:
                f.write(serialized_fig)
            
            cfig.after_export()
            print("save fig finish")
            print(time.time()-a)

    class ImportFigure(tornado.web.RequestHandler):
        def post(self):
            matplotlib.use('WebAgg')
            matplotlib.rcParams['agg.path.chunksize'] = 10000
            matplotlib.rcParams['path.simplify_threshold'] = 1

            import sys
            # 兼容旧版本的RadialTick类和MwThetaFormatter类的位置
            import TyPlotOnline.utility.mw_plotting_utils as mw_plotting_utils
            sys.modules['objects.mw_interface'] = mw_plotting_utils
            sys.path.append(os.path.dirname(TyPlotOnline.__file__))

            json_data = json.loads(self.request.body)
            filename = json_data.get('filename')
            userId = json_data.get('userId')
            if 'isCurrent' in json_data and json_data.get('isCurrent') is True:
                figId = json_data.get('figId')
                figId = int(figId)
                fig = self.application.figures[figId]["fig"]
                self.import_fig_current(filename, userId,fig)
            else:
                self.import_fig_new(filename, userId)
            # self.write({"status": True, "message": "Import figure successed."})


        def import_fig_new(self, filename, userId):
            plt.rcParams['toolbar'] = 'toolmanager'

            with open(filename, "rb") as f:
                serialized_fig = f.read()
                # cfig = dill.loads(serialized_fig)
                try:
                    cfig = syslab_loads(serialized_fig)
                except Exception as e:
                    if e.__str__() == "geomap":
                        self.write({"status": False, "message": "暂不支持导入地理图。"})
                        return
                file_base_name = os.path.basename(filename)
                # 读取文件时有异常会赋值cfig为None
                if cfig is None:
                    self.write({"status": False, "message": f"在新窗口打开文件失败：{file_base_name}文件格式有误。"})
                    return
                if "GlobalFont" in cfig.__dict__:
                    CGlobalSetting.cGlobalFont = cfig.__dict__["GlobalFont"]
                    del cfig.__dict__["GlobalFont"]

                
                if not isinstance(cfig,Figure):
                    cfig.after_import()
                    CGlobalSetting.c_fig_lst.append(cfig)
                    for cax in cfig.axs:
                        cax.after_import()
                # print(cfig.axs[0].__dict__)

                import io
                
                if not isinstance(cfig,Figure):
                    fig = cfig.fig
                else:
                    fig = cfig
                figId = id(fig)
                pic_IObytes = io.BytesIO()
                fig.savefig(pic_IObytes, format='png')
                pic_IObytes.seek(0)
                png_base64 = base64.b64encode(pic_IObytes.getvalue()).decode("utf-8").replace("\n", "")
                print("import figure: ", figId)
                # manager = init_figures(fig, figId)
                if not figId in self.application.figures:
                    self.application.figures[figId]=dict() 
                self.application.figures[figId]['png_base64'] = png_base64
                self.application.figures[figId]['fig']=fig
                # self.application.figures[figId]['manager']=manager
                print(self.application.figures[figId]['fig'])

                if not isinstance(cfig,Figure):
                    for cax in cfig.axs:
                        if mw_get_cfig(cax.fig).current_mplcursor == None:
                            mw_get_cfig(cax.fig).current_mplcursor = Cursor(cax.fig, cax.ax)
                        else:
                            mw_get_cfig(cax.fig).current_mplcursor.ax = cax.ax

                userHome = get_home_dir()
                # userId = os.environ['SYSLAB_ONLINE_USERID'] if 'SYSLAB_ONLINE_USERID' in os.environ else ""
                json_path = r"{0}/SyslabCloud/.syslab-oss/fig.json".format(userHome)

                if len(fig.axes) > 0 and fig.axes[0].get_title():
                    title = fig.axes[0].get_title()
                else:
                    # file_name = os.path.basename(filename)
                    file_name, ext = os.path.splitext(os.path.basename(filename))
                    print(file_name)
                    title = file_name
                    # title = "Python_Figure_" + str(fig.number)

                data = {"figId": figId, "webServer": True, "userId": userId, "title": title}
                with open(json_path, "w") as f:
                    json.dump(data, f)
                # if not CGlobalSetting.isOnline:

                # CGlobalSetting.c_fig_lst.append(cfig)
                    
            print("import fig finish")
            self.write({"status": True, "message": "Import figure successed."})

        def import_fig_current(self, filename, userId,fig):
            plt.rcParams['toolbar'] = 'toolmanager'
            cfig_current = mw_get_cfig(fig)
            with open(filename, "rb") as f:
                serialized_fig = f.read()
                # 在显示图形前禁用交互性
                plt.ioff()
                try:
                    cfig = syslab_loads(serialized_fig)
                except Exception as e:
                    if e.__str__() == "geomap":
                        self.write({"status": False, "message": "暂不支持导入地理图。"})
                        return
                file_base_name = os.path.basename(filename)
                # 读取文件时有异常会赋值cfig为None
                if cfig is None:
                    self.write({"status": False, "message": f"在当前窗口打开文件失败：{file_base_name}文件格式有误。"})
                    return
                type_mismatch = []
                if not isinstance(cfig,Figure):
                    plt.close(cfig.fig)
                    # 重新启用交互性
                    plt.ion()
                    for i in range(0,min(len(cfig_current.axs),len(cfig.axs))):
                        # 只允许直角坐标轴到直角坐标轴、极坐标轴到极坐标轴、三维坐标轴到三维坐标轴
                        if type(cfig_current.axs[i].ax.xaxis) != type(cfig.axs[i].ax.xaxis):
                            type_mismatch.append(i+1)
                            continue
                        if type(cfig_current.axs[i]) == CAxesYyaxis or type(cfig.axs[i]) == CAxesYyaxis:
                            continue
                        for c_line in cfig.axs[i].lines:
                            # 在添加前判断
                            had_data = cfig_current.axs[i].ax.has_data()
                            # 导入前属性处理
                            c_line.line.__dict__['_axes'] = None
                            c_line.line.__dict__['figure'] = None
                            c_line.line.__dict__['_transformSet'] = False
                            c_line.line.__dict__['_clippath'] = None
                            # 添加曲线到坐标轴
                            cfig_current.axs[i].ax.add_line(c_line.line)
                            # 更新c_line及c_line.line属性
                            cfig_current.axs[i].lines.append(c_line)
                            c_line.line.ax = cfig_current.axs[i].ax
                            c_line.line.figure = cfig_current.fig
                            c_line.ax = cfig_current.axs[i].ax
                            c_line.fig = cfig_current.fig
                            # 自动缩放
                            cfig_current.axs[i].ax._request_autoscale_view(scalex=cfig_current.axs[i].ax._autoscaleXon, scaley=cfig_current.axs[i].ax._autoscaleYon)
                            if type(c_line.line) == Line3D:
                                x,y,z=c_line.line.get_data_3d()
                                cfig_current.axs[i].ax.auto_scale_xyz(x,y,z,had_data=had_data)
                            # 属性补全 
                            # 不存在或者存在且为空的时候，需要处理
                            if not hasattr(c_line,"originDataX"):
                                c_line.originDataX = None
                                c_line.originDataY = None
                                c_line.sampled = False
                                c_line.init_origin_data()
                            elif hasattr(c_line,"originDataX") and c_line.originDataX is None:
                                c_line.init_origin_data()
                            if cfig_current.sampling:
                                cfig_current.axs[i].update_current_lim()
                                c_line.resample(cfig_current.axs[i].get_scale_factor())
                        for c_scatter in cfig.axs[i].scatters:
                            # 在添加前判断
                            had_data = cfig_current.axs[i].ax.has_data()
                            # 导入前属性处理
                            c_scatter.path_collection.__dict__['_axes'] = None
                            c_scatter.path_collection.__dict__['figure'] = None
                            c_scatter.path_collection.set_transform(mtransforms.IdentityTransform())
                            c_scatter.path_collection.__dict__['_transOffset'] = cfig_current.axs[i].ax.transData
                            c_scatter.path_collection.__dict__['_clippath'] = None
                            # 添加path_collection到坐标轴
                            cfig_current.axs[i].ax.add_collection(c_scatter.path_collection)
                            # 更新c_scatter及c_scatter.path_collection属性
                            cfig_current.axs[i].scatters.append(c_scatter)
                            c_scatter.path_collection.ax = cfig_current.axs[i].ax
                            c_scatter.path_collection.figure = cfig_current.fig
                            c_scatter.ax = cfig_current.axs[i].ax
                            c_scatter.fig = cfig_current.fig
                            # 自动缩放
                            cfig_current.axs[i].ax._request_autoscale_view()
                            if type(c_scatter.path_collection) == Path3DCollection:
                                _offsets3d = c_scatter.path_collection.__dict__['_offsets3d']
                                x = _offsets3d[0]
                                y = _offsets3d[1]
                                z = _offsets3d[2]
                                cfig_current.axs[i].ax.auto_scale_xyz(x,y,z,had_data=had_data)
                            # 属性补全 
                            # 不存在或者存在且为空的时候，需要处理
                            if not hasattr(c_scatter,"originDataX"):
                                c_scatter.originDataX = None
                                c_scatter.originDataY = None
                                c_scatter.sampled = False
                                c_scatter.init_origin_data()
                            elif hasattr(c_scatter,"originDataX") and c_scatter.originDataX is None:
                                c_scatter.init_origin_data()
                            if cfig_current.sampling:
                                cfig_current.axs[i].update_current_lim()
                                c_scatter.resample(cfig_current.axs[i].get_scale_factor())

                        update_legend(cfig_current.axs[i].ax)
                        # plt.savefig("testdavefig.syslabfig")
                        # plt.save_figure("testsavefig.syslabfig",cfig_current.fig) 
                else:
                    plt.close(cfig)
                    # 重新启用交互性
                    plt.ion()
                    for i in range(0,min(len(cfig.axes),len(cfig_current.axs))):
                        # 只允许直角坐标轴到直角坐标轴、极坐标轴到极坐标轴、三维坐标轴到三维坐标轴
                        if type(cfig_current.axs[i].ax.xaxis) != type(cfig.axes[i].xaxis):
                            type_mismatch.append(i+1)
                            continue
                        for line in cfig.axes[i].lines:
                            # 在添加前判断
                            had_data = cfig_current.axs[i].ax.has_data()
                            # 导入前属性处理
                            line.__dict__['_axes'] = None
                            line.__dict__['figure'] = None
                            line.__dict__['_transformSet'] = False
                            line.__dict__['_clippath'] = None
                            # 添加曲线到坐标轴
                            cfig_current.axs[i].ax.add_line(line)
                            # 初始化c_line
                            mw_update_clines(cfig_current.fig,[line])
                            # 更新line属性
                            line.ax = cfig_current.axs[i].ax
                            line.figure = cfig_current.fig
                            # 自动缩放
                            cfig_current.axs[i].ax._request_autoscale_view(scalex=cfig_current.axs[i].ax._autoscaleXon, scaley=cfig_current.axs[i].ax._autoscaleYon)
                            if type(line) == Line3D:
                                x,y,z=line.get_data_3d()
                                cfig_current.axs[i].ax.auto_scale_xyz(x,y,z,had_data=had_data)
                            if cfig_current.sampling:
                                cfig_current.axs[i].update_current_lim()
                                mw_get_cline(line).resample(cfig_current.axs[i].get_scale_factor())
                        for child in cfig.axes[i]._children:
                            if isinstance(child,PathCollection):
                                # 在添加前判断
                                had_data = cfig_current.axs[i].ax.has_data()
                                # 导入前属性处理
                                child.__dict__['_axes'] = None
                                child.__dict__['figure'] = None
                                child.set_transform(mtransforms.IdentityTransform())
                                child.__dict__['_transOffset'] = cfig_current.axs[i].ax.transData
                                child.__dict__['_clippath'] = None
                                # 添加PathCollection到坐标轴
                                cfig_current.axs[i].ax.add_collection(child)
                                # 初始化cscatter
                                mw_update_scatters(cfig_current.fig,[child])
                                # 更新PathCollection属性
                                child.ax = cfig_current.axs[i].ax
                                child.figure = cfig_current.fig
                                # 自动缩放
                                cfig_current.axs[i].ax._request_autoscale_view()
                                if type(child) == Path3DCollection:
                                    _offsets3d = child.__dict__['_offsets3d']
                                    x = _offsets3d[0]
                                    y = _offsets3d[1]
                                    z = _offsets3d[2]
                                    cfig_current.axs[i].ax.auto_scale_xyz(x,y,z,had_data=had_data)
                                if cfig_current.sampling:
                                    cfig_current.axs[i].update_current_lim()
                                    mw_get_cscatter(child).resample(cfig_current.axs[i].get_scale_factor())
                                cfig_current.fig.canvas.draw_idle()

                        update_legend(cfig_current.axs[i].ax)

                # 导入图窗坐标轴数量多于当前坐标轴数量时、坐标轴类型不一致时，提醒用户
                cur_ax_num = len(cfig_current.axs)
                if not isinstance(cfig,Figure):
                    ax_num = len(cfig.axs)
                else:
                    ax_num = len(cfig.axes)
                file_base_name = os.path.basename(filename)
                len_mismatch = len(type_mismatch)
                ax_ignore = []
                if ax_num > cur_ax_num:
                    ax_ignore = list(range(cur_ax_num + 1, ax_num + 1))
                title = "在当前窗口中打开"
                import_num = min(cur_ax_num,ax_num)-len_mismatch
                message = f"{file_base_name} 文件中有{ax_num}个坐标轴，已成功导入{import_num}个坐标轴。\n"
                
                if len_mismatch > 0:
                    message += "第"+"、".join([f"{index}" for index in type_mismatch]) + "个坐标轴导入失败，原因是与当前图窗对应坐标轴类型不一致。"
                if len(ax_ignore) > 0:
                    message += "第"+"、".join([f"{index}" for index in ax_ignore]) + "个坐标轴被忽略，原因是超过当前图窗坐标轴数量。"
                if not (len_mismatch == 0 and len(ax_ignore) == 0):
                    cfig_current.fig.canvas.send_event("show_dialog",title=title,message=message)

                # 坐标轴类型不一致的数量要比两个图窗坐标轴数量都少,才能在右下角显示导入成功
                if len(type_mismatch) < cur_ax_num and len(type_mismatch) < ax_num:
                    self.write({"status": True, "message": "Import figure successed."})

    def __init__(self):
        super(MyApplication, self).__init__([
            # Static files for the CSS and JS
            # (r'/_static/(.*)',
            # #(r'/(.*)',
            #  tornado.web.StaticFileHandler,
            #  {'path': FigureManagerWebAgg.get_static_file_path()}),

            # (r'/', MainPage),

            # The pages that contain the plot (or maybe the plots)
            # (r'/DataFrame\d', PlotPage),

            # (r'/mpl.js', self.MplJs),

            # Sends images and events to the browser, and receives
            # events from the browser
            (r'/([0-9]+)/ws', self.WebSocket),
            (r'/([0-9]+)/attribute/ws', self.AttributeWebSocket),
            # (r'/inner_con/([0-9]+)/ws', self.WebSocketInner),

            # Handles the downloading (i.e., saving) of static images
            (r'/download', self.Download),
            (r'/exportcsv', self.ExportCSV),
            (r'/initFigure', self.InitFigureHandler),
            (r'/initWebaggFigure', self.initWebaggFigureHandler),
            (r'/savePngBase64', self.SavePngBase64Handler),
            (r'/getPngBase64', self.GetPngBase64Handler),
            (r'/setActiveFigure', self.SetActiveFigureHandler),
            (r'/removeWebaggFigure', self.RemoveWebaggFigureHandler),
            (r'/updateFigure', self.UpdateFigureHandler),
            (r'/fileExists', self.FileExists),
            (r'/export_figure', self.ExportFigure),
            (r'/import_figure', self.ImportFigure)
            ]
            )

APPLICATION = MyApplication()
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(APPLICATION)
    # webagg_port = os.environ["SYSLAB_ONLINE_WEBAGGPORT"] if "SYSLAB_ONLINE_WEBAGGPORT" in os.environ else 8080
    if len(sys.argv)>1:
        webagg_port = int(sys.argv[1])
    else:
        webagg_port = 8080
    http_server.listen(webagg_port,'127.0.0.1')

    print("http://127.0.0.1:{0}/".format(webagg_port))
    print("Press Ctrl+C to quit")


    tornado.ioloop.IOLoop.instance().start()