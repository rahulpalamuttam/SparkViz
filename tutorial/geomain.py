from Backend.Utilities import Reader
from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

from Backend.Utilities import Sampling

N=1000
filtered_RDD = Reader.coordinates()
print len(filtered_RDD)
xs, ys = Sampling.sample_unzip(filtered_RDD, N)

map_options = GMapOptions(lat=30.29, lng=-97.73, map_type="roadmap", zoom=10)

scatter_plot = GMapPlot(
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
scatter_plot.add_glyph(source, circle)

scatter_plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
output_file("gmap_plot.html")
show(scatter_plot)