from bokeh.plotting import Figure, show, output_file
from bokeh.sampledata.us_states import data as states
from bokeh.client import push_session
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HBox






CONST_PATH_TO_FILE="resources/dataless.text"

dicts_from_file = []


color = ["blue", "red", "green", "gold", "black", "gray", "purple"]

ans = []
with open(CONST_PATH_TO_FILE,'r') as inf:
    for line in inf:
        dicts_from_file.append(eval(line)) 
        temp = eval(line)

        #dict2.append(zip(str(temp['group']),str(temp['geo'][0:7]), str(temp['geo'][1])))
        ans.append( (color[temp['group']],) + temp['geo'])



longitude = []
latitude = []
colors = []
for d in ans:
    longitude.append(d[1])
    latitude.append(d[2])
    colors.append(d[0])




session = push_session(curdoc())





del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")

state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]

state_xs = state_xs[0:5] + state_xs[6:16] + state_xs[17:18] + state_xs[19:31] + state_xs[32:46]
state_ys = state_ys[0:5] + state_ys[6:16] + state_ys[17:18] + state_ys[19:31] + state_ys[32:46]

x = [-100,-80, -70, -125, -100]
y = [30,40,45, 40, 45]
#color = ["blue", "red", "green", "gold", "black"]

source = ColumnDataSource(data=dict(x=state_xs, y=state_ys))
source2 = ColumnDataSource(data=dict(x=latitude, y=longitude, color=colors))

p = Figure(title="US Unemployment 2009", toolbar_location="left",
           plot_width=1100, plot_height=700)


p.patches('x', 'y', source=source, fill_alpha=0.1, line_width=1, line_alpha=0.3)
p.circle('x', 'y', color='color', source=source2, fill_alpha=0.1, line_width=1, line_alpha=0.001, size=3)

curdoc().add_root(HBox(children=[p], width=1100))
session.show()
session.loop_until_closed()