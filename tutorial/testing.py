from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

from Backend import DB

DB.__init__()




SAMPLE_SIZE = 1000
xs, ys = DB.get_current(SAMPLE_SIZE)
source = ColumnDataSource(data=dict(x=xs, y=ys))

map_options = GMapOptions(lat=30.29, lng=-97.73, map_type="roadmap", zoom=11)

scatter_plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Plot of Stations"
)



circle = Circle(x="x", y="y", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
scatter_plot.add_glyph(source, circle)

scatter_plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")

print type(source)

show(scatter_plot)
