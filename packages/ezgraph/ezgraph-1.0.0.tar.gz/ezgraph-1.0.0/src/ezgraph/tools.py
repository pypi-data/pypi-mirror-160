import itertools
import math
from bokeh.plotting import figure, show
from bokeh.io import output_notebook


def generate_graph(cities, lats, longs, **kwargs):
    class _struct():
        def __init__(self, labels, edge_xs, edge_ys, text_xs, text_ys, distances, lats, longs, tour_xs=None, tour_ys=None):
            self._labels = labels
            self._edge_xs = edge_xs
            self._edge_ys = edge_ys
            self._tour_xs = tour_xs
            self._tour_ys = tour_ys
            self._text_xs = text_xs
            self._text_ys = text_ys
            self._distances = distances
            self._lats = lats
            self._longs = longs

        def has_tour(self):
            return tour_xs is not None
        
        def __str__(self):
            return "graphtools.Graph\n ⌊ Labels: {0}\n ⌊ Latitudes: {1}\n ⌊ Longitudes: {2}\n ⌊ Edges: {3} {4}\n ⌊ Texts: {5} {6}\n ⌊ Distances: {7}\n ⌊ Tour: {8} {9}".format(self._labels, self._lats, self._longs, self._edge_xs, self._edge_ys, self._text_xs, self._text_ys, self._distances, self._tour_xs, self._tour_ys)

    cmap = {}
    tour = []
    scale = 1
    for key, value in kwargs.items():
        if key == "cmap": cmap = value
        if key == "tour":
            c = 0
            for i in range(len(value)):
                tour.append(value[i])
                if c > 0 and c < len(value)-1:
                    tour.append(value[i])
        if key == "scale": scale = value

    edge_xs = [list(pair) for pair in itertools.combinations(lats, 2)]
    edge_xs = list(itertools.chain(*edge_xs))
    edge_ys = [list(pair) for pair in itertools.combinations(longs, 2)]
    edge_ys = list(itertools.chain(*edge_ys))
    text_xs = [(edge_xs[i] + edge_xs[i+1])/2 for i in range(0, len(edge_xs), 2)]
    text_ys = [(edge_ys[i] + edge_ys[i+1])/2 for i in range(0, len(edge_ys), 2)]
    distances = ["{:.1f}".format(math.dist([edge_xs[i], edge_ys[i]], [edge_xs[i+1], edge_ys[i+1]])*scale) for i in range(0, len(edge_xs), 2)]
    labels = cities
    tour_xs = None
    tour_ys = None
    if len(cmap) > 1:
        keylist = list(cmap.keys())
        labels = [keylist[list(cmap.values()).index(c)] for c in cities]
        if len(tour) > 1:
            tour_xs = [lats[cities.index(cmap[city])] for city in tour]
            tour_ys = [longs[cities.index(cmap[city])] for city in tour]

    return _struct(labels, edge_xs, edge_ys, text_xs, text_ys, distances, lats, longs, tour_xs, tour_ys)


def draw_graph(gph, **kwargs):
    output_notebook()
    p = figure(title=(kwargs["title"] if "title" in kwargs else ""), toolbar_location="left", plot_width=550, plot_height=350)

    p.line(gph._edge_xs, gph._edge_ys, line_alpha=0.8, line_color='blue', line_width=1.5)
    if gph.has_tour():
        p.line(gph._tour_xs, gph._tour_ys, line_alpha=1, line_color='lawngreen', line_width=1.5)
    p.text(gph._text_xs, gph._text_ys, text=gph._distances, text_color='blue')
    p.circle(gph._lats, gph._longs, size=10, color='red', alpha=1)
    p.text(gph._lats, gph._longs, text=gph._labels)

    show(p)
