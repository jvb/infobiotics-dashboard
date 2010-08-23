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

def colour(i):
    return colours[int(i) % len(colours)]
