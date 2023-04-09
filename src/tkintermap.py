import tkinter as tk
import tkintermapview
from geopy.distance import geodesic
import networkx as nx
import UCS
import ASTAR

# create tkinter window
root_tk = tk.Tk()
root_tk.geometry(f"{1000}x{1000}")
root_tk.title("map_view_example.py")

# start and end entry
# create label
frame = tk.Frame(root_tk)
frame.pack(side=tk.TOP, pady=10)

path_label = tk.Label(frame, text = "Start node: (number)")
path_label.pack(side= tk.LEFT)

start_entry = tk.Entry(frame, width=5)
start_entry.pack(side=tk.LEFT)

# create label
path_label = tk.Label(frame, text = "End node: (number)")
path_label.pack(side= tk.LEFT)

end_entry = tk.Entry(frame, width=5)
end_entry.pack(side=tk.LEFT)


# ========== ALL NEW ADDED ELEMENTS AND FUNCTION ==========

# =========== GLOBALS ========= 
# remember to move when integrating
count = 0
savedcoordinates = 0
is_coordinate_saved = False
is_path_enabled = False
G = nx.Graph()
node_coords = {}

# ===== ALGORITHM BUTTONS AND FUNCTIONS =====

# ===== UCS =====
def ucsCall():
    global G
    for i in G.edges():
        map_widget.set_path([node_coords[i[0]],node_coords[i[1]]])
    
    ucs_path = UCS.UCS(G,start_entry.get(),end_entry.get())
    
    for i in range(len(ucs_path)-1):
        path = map_widget.set_path([node_coords[ucs_path[i]], node_coords[ucs_path[i+1]]],color = "green")
        
ucs_button = tk.Button(root_tk, text="UCS", command=ucsCall)
ucs_button.pack(side=tk.TOP, padx=10)

# ===== ASTAR =====
def astarCall():
    global G
    global node_coords
    
    for i in G.edges():
        map_widget.set_path([node_coords[i[0]],node_coords[i[1]]])
    
    astar_path = ASTAR.ASTAR(G,start_entry.get(),end_entry.get(),node_coords)
    
    for i in range(len(astar_path)-1):
        path = map_widget.set_path([node_coords[astar_path[i]], node_coords[astar_path[i+1]]],color = "green")

astar_button = tk.Button(root_tk, text="A*", command=astarCall)
astar_button.pack(side=tk.TOP, padx=10)

# ===== MAPS AND UTILITIES =====

# if path making enabled : can click two markers in a row to create an edge
path_label = tk.Label(root_tk, text = "Path making disabled")
path_label.pack(side= tk.TOP)

# create map widget
map_widget = tkintermapview.TkinterMapView(root_tk, width=800, height=600, corner_radius=0)
map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# set current widget position and zoom
map_widget.set_position(-6.891480, 107.610657) 
map_widget.set_zoom(30)

## add marker option when right click
def add_marker_event(coords):
    global count
    global G
    global node_coords
    print("Add marker:", coords)
    count += 1
    node_name = str(count)
    new_marker = map_widget.set_marker(coords[0], coords[1], text=str(count),command=marker_clicked)
    G.add_node(node_name)
    node_coords[node_name]=coords

map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=add_marker_event,
                                        pass_coords=True)

## enable pathmatking option when right click
def enable_path():
    global path_label
    global is_path_enabled
    is_path_enabled = not is_path_enabled
    if is_path_enabled:
        path_label.config(text="Path making enabled")
    else:
        path_label.config(text="Path making disabled")

map_widget.add_right_click_menu_command(label="Toggle Pathmaking",
                                        command=enable_path,
                                        pass_coords=False)

## get a node index given a coordinate
def getKey(coordinate):
    global node_coords
    for key in node_coords:
        if node_coords[key] == coordinate:
            return key
    return -1

## function triggered when a marker is clicked
def marker_clicked(marker):
    global savedcoordinates
    global is_path_enabled
    global is_coordinate_saved
    
    if is_path_enabled:
        if not is_coordinate_saved:
            savedcoordinates = marker.position
            is_coordinate_saved = True
        else:
            if marker.position != savedcoordinates:
                c1 = marker.position
                c2 = savedcoordinates
                path = map_widget.set_path([c1, c2])
                G.add_edge(getKey(c1), getKey(c2), weight=geodesic(c1,c2).km)
                is_coordinate_saved = False

root_tk.mainloop()