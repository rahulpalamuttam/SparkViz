from bokeh.client import push_session
from bokeh.plotting import Figure, show, reset_output, vplot, hplot
from bokeh.models import ColumnDataSource, HBox
from bokeh.models.widgets import Slider
from bokeh.io import gridplot, vform, curdoc, output_notebook, output_server, push_notebook
from bokeh.embed import autoload_server, components
from Backend import DB
import MapPoints
import ChartMath


session = None
scatter_plot = None
source = None
state_source = ColumnDataSource(data=MapPoints.getStates('x', 'y'))
pie_chart_source = None
slider = None


def update_coordinates(attrname, old, name):
    global N
    xbeg, xend = scatter_plot.x_range.start, scatter_plot.x_range.end
    ybeg, yend = scatter_plot.y_range.start, scatter_plot.y_range.end
    time_bin = slider.value
    xs, ys, color, time = DB.fetch(xbeg, xend, ybeg, yend)

    if len(xs) > 0 and len(ys) > 0:
        source.data = dict(x=xs, y=ys, color=color)
        pie_chart_source.data = ChartMath.compute_color_distribution('x', 'y', 'color', color)

    print xbeg, xend
    print ybeg, yend


def show(sample_size):
    global session
    global scatter_plot
    global source
    global pie_chart_source
    global slider
    DB.__init__(sample_size)
    session = push_session(curdoc())
    xs, ys, color, time = DB.get_current()
    pie_chart_source = ColumnDataSource(data=ChartMath.compute_color_distribution('x', 'y', 'color', color))
    source = ColumnDataSource(data=dict(x=xs, y=ys, color=color))

    scatter_plot = Figure(plot_height=800,
                          plot_width=800,
                          title="Plot of Voters",
                          tools="pan, reset, resize, save, wheel_zoom",
                          )

    scatter_plot.circle('x', 'y', color='color', source=source, line_width=0, line_alpha=0.001, fill_alpha=0.1, size=15)
    scatter_plot.patches('x', 'y', source=state_source, fill_alpha=0.0, line_width=1, line_alpha=0.3)

    scatter_plot.x_range.on_change('end', update_coordinates)

    pie_chart_plot = Figure(plot_height=800,
                            plot_width=800,
                            title="Voter Distribution",
                            x_range=(-1, 1),
                            y_range=(-1, 1))
    pie_chart_plot.wedge(x=0, y=0, source=pie_chart_source, radius=1, start_angle="x", end_angle="y", color="color")
    slider = Slider(start=0, end=10, value=1, step=.1, title="Time")
    slider.on_change('value', update_coordinates)
    h = hplot(scatter_plot, pie_chart_plot)
    v = vplot(slider, h)
    curdoc().add_root(HBox(children=[v], width=2000, height=2500))

    session.show()
    #script = autoload_server(scatter_plot, session_id=session.id)
    session.loop_until_closed()
    #return script

