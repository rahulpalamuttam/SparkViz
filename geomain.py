from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

import Sampling
import Reader
N=1000
coordinate_cache = Reader.coordinates()
print len(coordinate_cache)
xs, ys = Sampling.sample_unzip(coordinate_cache, N)

map_options = GMapOptions(lat=30.29, lng=-97.73, map_type="roadmap", zoom=10)

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="Austin",
    plot_height=800,
    plot_width=1500,
)

source = ColumnDataSource(
    data=dict(
        lat=ys,
        lon=xs,
    )
)

circle = Circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
show(plot)