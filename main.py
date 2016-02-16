from bokeh.client import push_session
from bokeh.plotting import Figure, show, reset_output
from bokeh.models import ColumnDataSource, HBox
from bokeh.io import curdoc, output_notebook, output_server, push_notebook
from bokeh.embed import autoload_server
from bokeh.sampledata.us_states import data as states
#--------------------------------
del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")
state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]
state_xs = state_xs[0:5] + state_xs[6:16] + state_xs[17:18] + state_xs[19:31] + state_xs[32:46]
state_ys = state_ys[0:5] + state_ys[6:16] + state_ys[17:18] + state_ys[19:31] + state_ys[32:46]
#---------------------------------------------
import time

import DB

xs = None
ys = None
SAMPLE_SIZE = None
session = None
plot = None
source = None

QueryStack = []

def update_coordinates(attrname, old, name):
    global N
    global xs, ys
    xbeg, xend = plot.x_range.start, plot.x_range.end
    ybeg, yend = plot.y_range.start, plot.y_range.end
    QueryStack.append((xbeg, xend, ybeg, yend, time.time() * 1000))
    # filtered = filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg, coordinate_cache)
    xs, ys = DB.fetch(xbeg, xend, ybeg, yend, SAMPLE_SIZE)

    if len(xs) > 0 and len(ys) > 0:
        source.data = dict(x=xs, y=ys)
    # print QueryStack
    print xbeg, xend
    print ybeg, yend

def printo():
    print "Callback"
    # global QueryStack
    #
    # if len(QueryStack) < 2:
    #     return
    #
    # cur_time = time.time() * 1000
    # xbeg, xend, ybeg, yend, epoch_time  = QueryStack[len(QueryStack) - 1]
    # xbeg1, xend1, ybeg1, yend1, epoch_time1  = QueryStack[len(QueryStack) - 2]
    #
    # if epoch_time - epoch_time1 > 100:
    #     QueryStack = []
    #     print epoch_time
    #     print epoch_time1
    #     xs, ys = DB.fetch(xbeg, xend, ybeg, yend, SAMPLE_SIZE)
    #
    #     if len(xs) > 0 and len(ys) > 0:
    #         source.data = dict(x=xs, y=ys)

def show(sample_size):
    global xs, ys
    global SAMPLE_SIZE
    global session
    global plot
    global source

    DB.__init__()
    #session = Session();
    session = push_session(curdoc())
    SAMPLE_SIZE = 1000
    xs, ys = DB.getCurrent(SAMPLE_SIZE)
    source = ColumnDataSource(data=dict(x=xs, y=ys))
    source2 = ColumnDataSource(data=dict(x=state_xs, y=state_ys))
    plot = Figure(plot_height=800,
              plot_width=800,
              title="Plot of Stations",
              tools="pan, reset, resize, save, wheel_zoom",
              )

    plot.circle('x', 'y', source=source, line_width=0, line_alpha=0.001, fill_alpha=0.2, size=15)
    plot.patches('x', 'y', source=source2, fill_alpha=0.1, line_width=1, line_alpha=0.3)

    plot.x_range.on_change('end', update_coordinates)
    # curdoc().add_periodic_callback(printo, 2000)
    curdoc().add_root(HBox(children=[plot], width=800))
    session.show()
    session.loop_until_closed()

