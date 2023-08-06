import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# ************************************************************************
# Module ivisit.matplotlib:
# Functions for easy inclusion of matplotlib plots in IVisit simulations 
# ************************************************************************

def getMatplotlibFigure(**kwargs):
    fig=Figure(**kwargs)
    return fig

def getMatplotlibImage(fig):    # return rgb image of matplotlib figure
    canvas=FigureCanvas(fig)
    canvas.draw()
    image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return image_from_plot

def getDataPos_from_PixelPos(pixel_x,pixel_y, canvas_h, ax=None, transData2Pixel=None):
    """ 
    transform pixel position within figure canvas to data position within matplotlib axis
    see also https://matplotlib.org/2.0.2/users/transforms_tutorial.html
            https://stackoverflow.com/questions/13662525/how-to-get-pixel-coordinates-for-matplotlib-generated-scatterplot
    """
    assert not(ax is None and transData2Pixel is None), "Parameters ax and transData2Pixel must not both be None!"
    if transData2Pixel is None: transData2Pixel=ax.transData.inverted()
    dataxy=transData2Pixel.transform([(pixel_x,canvas_h-pixel_y)])
    data_x=dataxy[0][0]
    data_y=dataxy[0][1]
    return data_x,data_y

def getDataPos_from_canvas(pixel_x,pixel_y,im_widget_canvas,ax=None, transData2Pixel=None):
    """ 
    transform pixel position within figure canvas to data position within matplotlib axis
    same as getDataPos_from_PixelPos, but simpler interface for ImageWidgets
    im_widget_canvas is binding object (i.e., the canvas of the image widget): it is returned by bind function display.bind2Widget(.) 
    Example: 
       (i) Do binding by 
           self.imw_canvas=display.bind2Widget("Trajectory","<Button-1>",self.onPressedB1_trajectory,"imgcanvas")
       (ii) do call to getDataPosImageWidget(.) by 
           data_x,data_y=getDataPos(self.clicked_x,self.clicked_y,self.imw_canvas,self.ax)
    see also https://matplotlib.org/2.0.2/users/transforms_tutorial.html
            https://stackoverflow.com/questions/13662525/how-to-get-pixel-coordinates-for-matplotlib-generated-scatterplot
    """
    return getDataPos_from_PixelPos(pixel_x,pixel_y, im_widget_canvas.winfo_height(), ax, transData2Pixel)
