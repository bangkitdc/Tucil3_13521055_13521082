# UCS and A* Algorithm Implementation to Determine the Shortest Path

<p align="center">
    <img src="https://github.com/bangkitdc/Tucil3_13521055_13521082/blob/main/assets/stima3.gif" width=800>
</p>

## About
Searching for the shortest distance between 2 nodes is a problem that has existed for a long time. The implementation of this problem can be seen in everyday life, such as on Google Maps. In this program, the problem is solved using the Uniform-Cost Search algorithm and the A* algorithm.

## Structure
```
.
├─── README.md
│     
├─── doc
│     └─── Tucil3_13521055_13521082.pdf
│
├─── test
│     ├─── test1.txt
│     ├─── test2.txt
│     ├─── test3.txt	
│     └─── test4.txt
|
├─── assets
│     └─── stima3.gif
│
└─── src
      ├─── main.py
      ├─── UCS.py
      └─── ASTAR.py
```

## Requirement Program
* Python newest version
* matplotlib
* networkx
* customtkinter, tkinter, tkintermapview

## How To Run
Run main.py in src directory using `cd src`, `python main.py`

## Test File Structure
* The test file represents a graph with N nodes. 
* The first N lines correspond to an N x N adjacency matrix. 
* The next line contains N strings separated by a space representing a node's name in order. 
* The final line contains N coordinates of each node in order with the structure of (<lat>,<lng>) where <lat> is the coordinate's latitude value and <lng> is the coordinate's longitude value.
* Note : a weighted matrix is not used due to it's redundancy (the coordinates implies weight for each edges)

## Authors
| Name                           | NIM      |
| ------------------------------ | -------- |
| Muhammad Bangkit Dwi Cahyono   | 13521055 |
| Farizki Kurniawan              | 13521082 |
