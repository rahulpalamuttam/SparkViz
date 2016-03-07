from bokeh.sampledata.us_states import data as states

del states["HI"]
del states["AK"]

EXCLUDED = ("ak", "hi", "pr", "gu", "vi", "mp", "as")
state_xs = [states[code]["lons"] for code in states]
state_ys = [states[code]["lats"] for code in states]
state_xs = state_xs[0:5] + state_xs[6:16] + state_xs[17:18] + state_xs[19:31] + state_xs[32:46]
state_ys = state_ys[0:5] + state_ys[6:16] + state_ys[17:18] + state_ys[19:31] + state_ys[32:46]


def getStates(x, y):
    return {x: state_xs, y: state_ys}