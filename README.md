alternative dijkstra implementation using incoming weights

<img src="./demo1.gif" width="300" height="300"/><img src="./demo2.gif" width="300" height="300"/>

| Control     | Color                                                   | Meaning             |
| ----------- | ------------------------------------------------------- | ------------------- |
|Left Mouse   |<code style="color:red">&#9724;Red                       |Start                |
|Right Mouse  |<code style="color:black">&#9724;Black                   |Wall                 |
|Middle Mouse |<code style="color:blue">&#9724;Blue                     |End                  |
|             |<code style="color:green">&#9724;Dark Green              |Reachable from Start |
|             |<code style="color:greenyellow">&#9724;Light Green       |Path to End          |
|Space        |                                                         |Reset Path           |

only requires pygame-ce

you can run either script, main has more functionality and can be played around with more features, grid_dijkstra was a mvp demo and shows relatively quick performance with heapq even with larger grids (which should be more than the general use case of something like this)
