from dateutil.parser import parse
colorDict = {0:'black', 1:'red', 2:'blue', 3:'yellow', 4:'green', 5:'pink', 6:'brown'}

def reading(DATA_PATH):
    dict = {}
    file = open(DATA_PATH, 'r')
    num = 0
    for line in file:
        dict[str(num)] = (eval(line))
        num += 1
    return dict

def tuplize(DATA_PATH):
    dict = reading(DATA_PATH)
    tuple_list = []
    for i in dict:
        entry = dict[i]
        y, x = entry['geo']
        time = entry['time']
        color = colorDict[entry['group']]
        tuple = (x, y, color, time)
        tuple_list.append(tuple)
    return tuple_list