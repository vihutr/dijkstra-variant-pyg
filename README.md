alternative dijkstra implementation using incoming weights

only requires pygame-ce

you can run either script, main has more functionality and can be played around with more features, grid_dijkstra was a mvp demo and shows relatively quick performance with heapq even with larger grids (which should be more than the general use case of something like this)

Current functionality of main.py:
left click to place your start
right click to place a wall (blocks path)
middle click to place end (after placing a start)

Default Legend:
Red = Start Point/ Path
Green = traversable from Start
Blue = End
