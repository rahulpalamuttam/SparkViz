from bokeh.client import push_session
from bokeh.plotting import Figure, show, reset_output, vplot, hplot
from bokeh.models import ColumnDataSource, HBox, VBox
from bokeh.models.widgets import Slider
from bokeh.io import gridplot, vform, curdoc, output_notebook, output_server, push_notebook
from bokeh.embed import autoload_server, components
from bokeh.charts import Line
from collections import Counter

from Backend import DB
import MapPoints
import ChartMath
import numpy as np

session = None
scatter_plot = None
source = None
state_source = ColumnDataSource(data=MapPoints.getStates('x', 'y'))
pie_chart_source = None
line_chart_source = None
slider = None


def update_coordinates(attrname, old, name):
    global N
    xbeg, xend = scatter_plot.x_range.start, scatter_plot.x_range.end
    ybeg, yend = scatter_plot.y_range.start, scatter_plot.y_range.end
    time_bin = slider.value
    xs, ys, color, time = DB.fetch(xbeg, xend, ybeg, yend, time_bin)

    if len(xs) > 0 and len(ys) > 0:
        xs = [xs[i] for i,v in enumerate(time) if time[i] == time_bin]
        ys = [ys[i] for i,v in enumerate(time) if time[i] == time_bin]
        color = [color[i] for i,v in enumerate(time) if time[i] == time_bin]
        source.data = dict(x=xs, y=ys, color=color)
        pie_chart_source.data = ChartMath.compute_color_distribution('x', 'y', 'color', color)
        time_dict = Counter(time)
        line_chart_source.data = dict(x=[key for key in time_dict], y=[time_dict[key] for key in time_dict])
        print time_dict
    else:
        source.data = dict(x=[], y=[], color=[])
        pie_chart_source.data = ChartMath.compute_color_distribution('x', 'y', 'color', [])
    print xbeg, xend
    print ybeg, yend


def show(sample_size):
    global session
    global scatter_plot
    global source
    global pie_chart_source
    global line_chart_source
    global slider
    DB.__init__(sample_size)
    min_time = DB.min_time()
    max_time = DB.max_time()
    print min_time
    print min_time
    xs, ys, color, time = DB.get_current()
    xs = [xs[i] for i,v in enumerate(time) if time[i] == min_time]
    ys = [ys[i] for i,v in enumerate(time) if time[i] == min_time]
    color = [color[i] for i,v in enumerate(time) if time[i] == min_time]

    time_dict = Counter(time)
    pie_chart_source = ColumnDataSource(data=ChartMath.compute_color_distribution('x', 'y', 'color', color))
    line_chart_source = ColumnDataSource(data=dict(x=[key for key in time_dict], y=[time_dict[key] for key in time_dict]))
    source = ColumnDataSource(data=dict(x=xs, y=ys, color=color))

    scatter_plot = Figure(plot_height=800,
                          plot_width=1200,
                          title="Plot of Voters",
                          tools="pan, reset, resize, save, wheel_zoom",
                          )

    scatter_plot.circle('x', 'y', color='color', source=source, line_width=0, line_alpha=0.001, fill_alpha=0.5, size=15)
    scatter_plot.patches('x', 'y', source=state_source, fill_alpha=0.1, line_width=3, line_alpha=1)

    scatter_plot.x_range.on_change('end', update_coordinates)
    line_chart = Figure(title="Distribution over Time", plot_width=350, plot_height=350)
    line_chart.line(x='x', y='y', source=line_chart_source)
    pie_chart_plot = Figure(plot_height=350,
                            plot_width=350,
                            title="Voter Distribution",
                            x_range=(-1, 1),
                            y_range=(-1, 1))
    pie_chart_plot.wedge(x=0, y=0, source=pie_chart_source, radius=1, start_angle="x", end_angle="y", color="color")
    slider = Slider(start=min_time, end=max_time, value=min_time, step=1, title="Time")

    slider.on_change('value', update_coordinates)
    h = hplot(scatter_plot, vplot(pie_chart_plot, line_chart))
    vplot(slider, h, width=1600, height=1800)
    session = push_session(curdoc())
    session.show()
    #script = autoload_server(scatter_plot, session_id=session.id)
    session.loop_until_closed()
    #return script

