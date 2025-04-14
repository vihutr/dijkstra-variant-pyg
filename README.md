alternative dijkstra implementation using incoming weights

<img src="./demo1.gif" width="300" height="300"/><img src="./demo2.gif" width="300" height="300"/>

| Control     | Color                                                      | Meaning             |
| ----------- | ---------------------------------------------------------- | ------------------- |
|Left Mouse   |<span style="color:rgb(255,0,0)">&#9724;</span>Red          |Start                |
|Right Mouse  |<span style="color:rgb(0,0,0)">&#9724;</span>Black          |Wall                 |
|Middle Mouse |<span style="color:rgb(10,10,255)">&#9724;</span>Blue       |End                  |
|             |<span style="color:rgb(20,100,0)">&#9724;</span>Dark Green  |Reachable from Start |
|             |<span style="color:rgb(20,255,15)">&#9724;</span>Light Green|Path to End          |
|Space        |                                                            |Reset Path           |

only requires pygame-ce

you can run either script, main has more functionality and can be played around with more features, grid_dijkstra was a mvp demo and shows relatively quick performance with heapq even with larger grids (which should be more than the general use case of something like this)
