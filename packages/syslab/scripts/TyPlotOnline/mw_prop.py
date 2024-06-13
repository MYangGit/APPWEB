from TyPlotOnline.objects.mw_interface import *
from TyPlotOnline.mw_actions import editmode_enable
from TyPlotOnline.objects.mw_global_setting import CGlobalSetting

def before_set_prop(event):
    if event["label"] == "copy":
        CGlobalSetting.line_copy_prop.clear()   

def mw_set_prop(event):
    before_set_prop(event)
    name = event["label"]
    value = event["value"]
    cfig = mw_get_cfig()
    cfig.set_current_objs_prop(name, value)


def mw_delete_current_datatip(event):
    cfig = mw_get_cfig()
    cfig.current_mplcursor.delete_current()
    update_view()


def mw_delete_all_datatips(event):
    cfig = mw_get_cfig()
    cfig.current_mplcursor.delete_all()
    update_view()


import sys
import tornado.ioloop
def mw_close_webserver():
    tornado.ioloop.IOLoop.current().stop()
    sys.exit()


def mw_property_init(event):
    print("property_init")
    fig = plt.gcf()
    cfig = mw_get_cfig(fig)
    current_objs = cfig.current_objs
    
    if len(current_objs) > 0 and cfig.edit_mode:
        fig.canvas.send_event("edit_finish")
    elif len(cfig.axs) > 0:
        editmode_enable(fig)
        mw_clear_status()
        cax = mw_get_cax(fig.gca())
        cax.pick_self()
        fig.canvas.send_event("edit_finish")  
    else:
        editmode_enable(fig)
        fig.canvas.send_event("edit_finish")

def mw_property_ready(event):
    prop_class={
        "CLine":"Line",
        "CScatter":"Scatter",
        "CDTextBox":"TextBox",
        "CTitle":"Text",
        "CXlabel":"Text",
        "CYlabel":"Text",
        "CZlabel":"Text",
        "CDEllipse":"Ellipse",
        "CDDoubleArrow":"Line",
        "CDTextArrow":"Line",
        "CDRectangle":"Rectangle",
        "CDArrow":"Line",
        "CDLine":"Line",
        "CAxes":"Axes",
        "CAxesYyaxis":"Axes",
        "CFigure":"Figure"
    }
    fig = plt.gcf()
    cfig = mw_get_cfig(fig)
    current_objs = cfig.current_objs

    props = {}
    current_prop = "Axes"
    if len(current_objs) > 0 and cfig.edit_mode:
        obj = current_objs[0]
        if obj.__class__.__name__ not in prop_class:
            obj = cfig
        if obj.__class__.__name__ == "CFigure":
            cax = None
            cobj = None
            axs = obj.get_all_axes()
            if len(axs) > 0:
                cax = mw_get_cax()
                if len(cax.lines) > 0:
                    cobj = cax.lines[0]

            props = get_property(cfig = obj, cax = cax, cobj = cobj, obj_name = "Line")
            current_prop = "Figure"
        elif obj.__class__.__name__ == "CAxes" or obj.__class__.__name__ == "CAxesYyaxis":
            cobj = None
            if len(obj.lines) > 0:
                cobj = obj.lines[0]

            props = get_property(cfig = cfig, cax = obj, cobj = cobj, obj_name = "Line")
            current_prop = "Axes"
        else:
            cax = mw_get_cax()
            props = get_property(cfig = cfig, cax = cax, cobj = obj, obj_name = prop_class[obj.__class__.__name__])
            current_prop = prop_class[obj.__class__.__name__]
        fig.canvas.send_event("property_ready", props=props, current_prop=current_prop, font_list = get_font_lst())
    elif len(cfig.axs) > 0:
        
        cobj = None
        obj_name = ""
        cax = mw_get_cax(fig.gca())
        if len(cax.lines) > 0:
            cobj = cax.lines[0]
            obj_name = "Line"

        props = get_property(cfig = cfig, cax = cax, cobj = cobj, obj_name = obj_name)
        current_prop = "Axes"
        fig.canvas.send_event("property_ready", props=props, current_prop=current_prop, font_list = get_font_lst())
    else:
        props = get_property(cfig = cfig)
        current_prop = "Figure"
        fig.canvas.send_event("property_ready", props=props, current_prop=current_prop, font_list = get_font_lst())


def mw_change_select_objs(event):
    print("mw_change_select_objs========",event)
    mw_clear_status()
    name = event["name"]
    
    fig = plt.gcf()
    cfig = mw_get_cfig(fig)

    # 前端名称为textbox，cfig.prop_objs内为TextBox
    if name == "textbox":
        name = "TextBox"
    if name in cfig.prop_objs:
        obj = cfig.prop_objs[name]
        obj.pick_self()

def mw_property_close(event):
    fig = plt.gcf()
    cfig = mw_get_cfig(fig)

    cfig.prop_objs = {}

def mw_get_linestyle_list(event):
    lst_style = ['-', '--', '-.', ':', 'None']

    return {"linestyle": lst_style}

def mw_get_linestyle_list_contextmenu(event):
    lst_style = ['实线', '虚线', '点线', '点划线', '无']

    return {"linestyle": lst_style}

def mw_get_font_list():
    lst_font = get_font_lst()

    return {"font", lst_font}

def mw_get_marker_list(event):
    lst_marker = ['+', 'o', '.', 'x', 'square', 'diamond', 'v', 
                   '^', '>', '<', 'pentagram', '|', '_', 'none']
    
    return {"marker": lst_marker}

def mw_get_marker_list_contextmenu(event):
    lst_marker = ['+', 'o', '.', 'x', '四方形', '菱形', 'v', 
                   '^', '>', '<', '五角形', '无']
    
    return {"marker": lst_marker}

def mw_get_marker_size(event):
    pass
