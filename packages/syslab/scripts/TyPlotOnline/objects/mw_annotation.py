import logging
import numpy as np
import matplotlib.transforms as mtransforms
from matplotlib.text import Text,Annotation,_AnnotationBase
from matplotlib.patches import FancyArrowPatch
from matplotlib import cbook


_log = logging.getLogger(__name__)

def mw_annotate(ax, text, xy,linecolors, *args, **kwargs):
        a = mw_Annotation(text, xy,linecolors, *args, **kwargs)
        a.set_transform(mtransforms.IdentityTransform())
        if 'clip_on' in kwargs:
            a.set_clip_path(ax.patch)
        ax._add_text(a)
        return a

class mw_Text(Text):
    def __init__(self,
                 x=0, y=0, text='',
                 linecolors=None,
                 **kwargs
                 ):
        Text.__init__(self,x,y,text,**kwargs)
        self._linecolors=[]
        if linecolors!=None:
            self._linecolors.insert(0,'black')

    def init_linecolors(self):
        self._linecolors.clear()
        self._linecolors.insert(0,'black')


    def draw(self, renderer):
        # docstring inherited

        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible():
            return
        if self.get_text() == '':
            return

        renderer.open_group('text', self.get_gid())

        with self._cm_set(text=self._get_wrapped_text()):
            bbox, info, descent = self._get_layout(renderer)
            trans = self.get_transform()

            # don't use self.get_position here, which refers to text
            # position in Text:
            posx = float(self.convert_xunits(self._x))
            posy = float(self.convert_yunits(self._y))
            posx, posy = trans.transform((posx, posy))
            if not np.isfinite(posx) or not np.isfinite(posy):
                _log.warning("posx and posy should be finite values")
                return
            canvasw, canvash = renderer.get_canvas_width_height()

            # Update the location and size of the bbox
            # (`.patches.FancyBboxPatch`), and draw it.
            if self._bbox_patch:
                self.update_bbox_position_size(renderer)
                self._bbox_patch.draw(renderer)

            gc = renderer.new_gc()
            gc.set_foreground(self.get_color())
            gc.set_alpha(self.get_alpha())
            gc.set_url(self._url)
            self._set_gc_clip(gc)

            linecount=0

            angle = self.get_rotation()

            for line, wh, x, y in info:

                mtext = self if len(info) == 1 else None
                x = x + posx
                y = y + posy
                if renderer.flipy():
                    y = canvash - y
                clean_line, ismath = self._preprocess_math(line)

                if self.get_path_effects():
                    from matplotlib.patheffects import PathEffectRenderer
                    textrenderer = PathEffectRenderer(
                        self.get_path_effects(), renderer)
                else:
                    textrenderer = renderer

                if self.get_usetex():
                    textrenderer.draw_tex(gc, x, y, clean_line,
                                          self._fontproperties, angle,
                                          mtext=mtext)
                elif self._linecolors!=None:
                    gc.set_foreground(self._linecolors[linecount])

                    textrenderer.draw_text(gc, x, y, clean_line,
                                           self._fontproperties, angle,
                                           ismath=ismath, mtext=mtext)

                else:
                    textrenderer.draw_text(gc, x, y, clean_line,
                                           self._fontproperties, angle,
                                           ismath=ismath, mtext=mtext)
                linecount+=1

        gc.restore()
        renderer.close_group('text')
        self.stale = False


class mw_Annotation(Annotation,mw_Text):

    def __init__(self, text, xy,
            linecolors=None,
            xytext=None,
            xycoords='data',
            textcoords=None,
            arrowprops=None,
            annotation_clip=None,
            **kwargs):

        _AnnotationBase.__init__(self,
                                 xy,
                                 xycoords=xycoords,
                                 annotation_clip=annotation_clip)
        # warn about wonky input data
        if (xytext is None and
                textcoords is not None and
                textcoords != xycoords):
            cbook._warn_external("You have used the `textcoords` kwarg, but "
                                 "not the `xytext` kwarg.  This can lead to "
                                 "surprising results.")

        # clean up textcoords and assign default
        if textcoords is None:
            textcoords = self.xycoords
        self._textcoords = textcoords

        # cleanup xytext defaults
        if xytext is None:
            xytext = self.xy
        x, y = xytext

        self.arrowprops = arrowprops
        if arrowprops is not None:
            arrowprops = arrowprops.copy()
            if "arrowstyle" in arrowprops:
                self._arrow_relpos = arrowprops.pop("relpos", (0.5, 0.5))
            else:
                # modified YAArrow API to be used with FancyArrowPatch
                for key in [
                        'width', 'headwidth', 'headlength', 'shrink', 'frac']:
                    arrowprops.pop(key, None)
            self.arrow_patch = FancyArrowPatch((0, 0), (1, 1), **arrowprops)
        else:
            self.arrow_patch = None

        # Must come last, as some kwargs may be propagated to arrow_patch.
        mw_Text.__init__( self,x, y, text,linecolors=linecolors ,**kwargs)


    def draw(self, renderer):
        # docstring inherited
        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible() or not self._check_xy(renderer):
            return
        # Update text positions before `Text.draw` would, so that the
        # FancyArrowPatch is correctly positioned.
        self.update_positions(renderer)
        self.update_bbox_position_size(renderer)
        if self.arrow_patch is not None:   # FancyArrowPatch
            if self.arrow_patch.figure is None and self.figure is not None:
                self.arrow_patch.figure = self.figure
            self.arrow_patch.draw(renderer)
        # Draw text, including FancyBboxPatch, after FancyArrowPatch.
        # Otherwise, a wedge arrowstyle can land partly on top of the Bbox.
        mw_Text.draw(self, renderer)
