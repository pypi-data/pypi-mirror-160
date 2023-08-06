EZGraph
========
EZGraph is a helper library for fast construction of graphs and networks for visual purposes based on Bokeh.js. The EZGraph library simplifies the process of drawing graphs for demonstrations by introducing high-level functions that take care of creating the appropriate data structures for the Bokeh.js backend. It is currently not intended for public use because of its limited number of functions.

Installing
========
.. code-block:: bash

    pip install ezgraph

Usage
========
.. code-block:: bash

    import ezgraph as ezg
    
    cities = ["Köln", "Berlin", "Leipzig", "Hamburg"]
    latitudes = [50.935173, 52.520008, 51.3396955, 53.551085]
    longitudes = [6.953101, 13.404954, 12.3730747, 9.993682]
    cmap = {"A": "Köln", "B": "Berlin", "C": "Leipzig", "D": "Hamburg"}
    tour = ["A", "B", "D", "C", "A"]
    
    graph = ezg.generate_graph(cities, latitudes, longitudes, cmap=cmap, tour=tour)
    ezg.draw_graph(graph, title="An example TSP of n=4 with a possible solution")
