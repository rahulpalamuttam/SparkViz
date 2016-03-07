from bokeh.plotting import *
from numpy import pi

# define starts/ends for wedges from percentages of a circle
percents = [0, 0.3, 0.4, 0.6, 0.9, 1]
starts = [p*2*pi for p in percents[:-1]]
ends = [p*2*pi for p in percents[1:]]
colors = ["red", "green", "blue", "orange", "yellow"]
print colors
print starts
print ends
source = ColumnDataSource(data=dict(x=starts, y=ends, color=colors))
# a color for each pie piece


p = figure(x_range=(-1,1), y_range=(-1,1))

p.wedge(x=0, y=0, source=source, radius=1, start_angle="x", end_angle="y", color="color")

# display/save everythin
output_file("pie.html")
show(p)