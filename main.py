import random
from bokeh.client import push_session
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HBox
from bokeh.io import curdoc

import Reader
import Sampling
import DB

DB.__init__()

session = push_session(curdoc())
SAMPLE_SIZE = 1000
xs, ys = DB.getCurrent(SAMPLE_SIZE)
source = ColumnDataSource(data=dict(x=xs, y=ys))
plot = Figure(plot_height=800,
              plot_width=900,
              title="Plot of Stations",
              tools="pan, reset, resize, save, wheel_zoom")

plot.circle('x', 'y', source=source, line_width=3, line_alpha=0.6)


def update_coordinates(attrname, old, name):
    global N
    global xs, ys
    xbeg, xend = plot.x_range.start, plot.x_range.end
    ybeg, yend = plot.y_range.start, plot.y_range.end
    #filtered = filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg, coordinate_cache)
    xs, ys = DB.fetch(xbeg, xend, ybeg, yend, SAMPLE_SIZE)

    if len(xs) > 0 and len(ys) > 0:
        source.data = dict(x=xs, y=ys)

    print xbeg, xend
    print ybeg, yend


plot.x_range.on_change('end', update_coordinates)
curdoc().add_root(HBox(children=[plot], width=800))
session.show()
session.loop_until_closed()
