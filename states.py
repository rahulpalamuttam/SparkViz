from bokeh.plotting import Figure, show, output_file
from bokeh.sampledata.us_states import data as states
from bokeh.client import push_session
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HBox

session = push_session(curdoc())

del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]
source = ColumnDataSource(data=dict(x=state_xs, y=state_ys))

p = Figure(title="US Unemployment 2009", toolbar_location="left",
           plot_width=1100, plot_height=700)
#plot.circle('x', 'y', source=source, line_width=3, line_alpha=0.6)
p.circle('x', 'y', source=source, fill_alpha=0.0, line_width=1, line_alpha=0.3)


curdoc().add_root(HBox(children=[p], width=1100))
session.show()
session.loop_until_closed()