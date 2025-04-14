alternative dijkstra implementation using incoming weights

<img src="./demo1.gif" width="400" height="400" />
<img src="./demo2.gif" width="400" height="400" />

Controls/Legend:
Left Click: Red = Start Point/ Path
Right Click: Black = Wall
Middle Click: Blue = End
Green = traversable from Start/Red

only requires pygame-ce

you can run either script, main has more functionality and can be played around with more features, grid_dijkstra was a mvp demo and shows relatively quick performance with heapq even with larger grids (which should be more than the general use case of something like this)
