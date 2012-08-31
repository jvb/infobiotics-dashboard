#http://en.wikipedia.org/wiki/X11_color_names
colours = ['blue', 'red', 'gold', 'green', 'darkorchid', 'darkorange',
           'mediumturquoise', 'deeppink', 'chartreuse', 'brown', 'teal',
           'tomato', 'goldenrod', 'indigo', 'cornflowerblue', 'darkseagreen',
           'bisque', 'blueviolet',
           'burlywood', 'cadetblue',
           'chocolate', 'coral', 'cornflowerblue',
           'crimson', 'darkcyan', 'darkgoldenrod', 'darkkhaki',
           'darkmagenta', 'darkolivegreen',
           'darkseagreen', 'darkslategrey', 'deepskyblue',
           'greenyellow', 'indigo', 'khaki',
           'lavender', 'orangered', 'palevioletred',
           'royalblue', 'yellowgreen', 'darkblue',
           'darkgreen', 'darkred']

#TODO http://www.omatrix.com/manual/gcolor.htm Unless specified by gcolor, O-Matrix uses the following sequence of colors for plotting: "black", "maroon", "green", "olive", "navy", "purple", "teal", "gray", "silver", "red", "lime", "yellow", "blue", "fuschia", and "aqua". That is, the first line plotted with gplot will be black, the second will be maroon, and so on. The sequence starts over after an aqua plot.

def colour(i):
    return colours[int(i) % len(colours)]


markers = [
#    '.',',',
    'o',
    'v', '^', '<', '>',
#    '1','2','3','4',
    's', 'p', '*', 'h',
    'H',
    '+', 'x',
    'D',
    'd',
#    '|','_',
]

def marker(i):
    return markers[int(i) % len(markers)]
