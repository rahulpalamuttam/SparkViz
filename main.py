from bokeh.client import push_session
from bokeh.plotting import Figure, show, reset_output, vplot, hplot
from bokeh.models import ColumnDataSource, HBox
from bokeh.io import curdoc, output_notebook, output_server, push_notebook
from bokeh.embed import autoload_server, components
from bokeh.sampledata.us_states import data as states

from collections import Counter
from numpy import pi
#--------------------------------
del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")
state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]
state_xs = state_xs[0:5] + state_xs[6:16] + state_xs[17:18] + state_xs[19:31] + state_xs[32:46]
state_ys = state_ys[0:5] + state_ys[6:16] + state_ys[17:18] + state_ys[19:31] + state_ys[32:46]
#---------------------------------------------
percents = [0, 0.3, 0.4, 0.6, 0.9, 1]
starts = [p*2*pi for p in percents[:-1]]
ends = [p*2*pi for p in percents[1:]]
colors = ["red", "green", "blue", "orange", "yellow", "black", "pink", "brown"]
source3 = ColumnDataSource(data=dict(x=starts, y=ends, color=colors))
#------------------------------------------------------------------------
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
    global colors
    xbeg, xend = plot.x_range.start, plot.x_range.end
    ybeg, yend = plot.y_range.start, plot.y_range.end
    #QueryStack.append((xbeg, xend, ybeg, yend, time.time() * 1000))
    # filtered = filter(lambda pr: xend > pr[0] > xbeg and yend > pr[1] > ybeg, coordinate_cache)
    xs, ys, color = DB.fetch(xbeg, xend, ybeg, yend, SAMPLE_SIZE)

    if len(xs) > 0 and len(ys) > 0:
        lenum = len(color)
        color_counts = Counter(color)
        percents = [0]
        for key in colors:
            aggregate = percents[-1] + color_counts[key]/float(lenum)
            percents.append(aggregate)

        starter = [perc*2*pi for perc in percents[:-1]]
        ender = [perc*2*pi for perc in percents[1:]]
        print color_counts
        print percents
        source.data = dict(x=xs, y=ys, color=color)
        source3.data = dict(x=starter, y=ender, color=colors)
        # process colors
    # print QueryStack
    print xbeg, xend
    print ybeg, yend



def show(sample_size):
    global xs, ys
    global SAMPLE_SIZE
    global session
    global plot
    global source
    global source3
    DB.__init__()
    #session = Session();
    session = push_session(curdoc())
    SAMPLE_SIZE = sample_size
    xs, ys, color = DB.getCurrent(SAMPLE_SIZE)
    lenum = len(color)
    color_counts = Counter(color)
    percents = [0]
    for key in colors:
        aggregate = percents[-1] + color_counts[key]/float(lenum)
        percents.append(aggregate)

    starter = [perc*2*pi for perc in percents[:-1]]
    ender = [perc*2*pi for perc in percents[1:]]
    print color_counts
    print percents
    source3 = ColumnDataSource(data=dict(x=starter, y=ender, color=colors))
    source = ColumnDataSource(data=dict(x=xs, y=ys, color=color))
    source2 = ColumnDataSource(data=dict(x=state_xs, y=state_ys))
    plot = Figure(plot_height=800,
              plot_width=800,
              title="Plot of Voters",
              tools="pan, reset, resize, save, wheel_zoom",
              )

    plot.circle('x', 'y', color='color', source=source, line_width=0, line_alpha=0.001, fill_alpha=0.1, size=15)
    plot.patches('x', 'y', source=source2, fill_alpha=0.0, line_width=1, line_alpha=0.3)

    plot.x_range.on_change('end', update_coordinates)

    # curdoc().add_periodic_callback(printo, 2000)p = figure(x_range=(-1,1), y_range=(-1,1))
    p = Figure(plot_height=800,
              plot_width=800,
              title="Voter Distribution",
                x_range=(-1,1),
               y_range=(-1,1))

    p.wedge(x=0, y=0, source=source3, radius=1, start_angle="x", end_angle="y", color="color")
    curdoc().add_root(HBox(children=[plot, p], width=1600))
    session.show()
    script = autoload_server(plot, session_id=session.id)
    session.loop_until_closed()
    return script

