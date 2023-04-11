import networkx as nx
import matplotlib.pyplot as plt
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import UCS
import ASTAR
from tkintermapview import TkinterMapView
from geopy.distance import geodesic
from math import radians, sin, cos, sqrt, atan2

class GraphVisualizer:
    def __init__(self):
        self.window = Tk()

        self.window.title("Shortest Path Visualizer")
        self.window.geometry("1080x600")
        self.window.configure(bg = "#FFFFFF")
        self.window.resizable(False, False)

        self.bonus = False
        self.countMarker = 0
        self.savedcoordinates = 0
        self.is_coordinate_saved = False
        self.is_path_enabled = False

        self.G = None
        self.node_coords = {}
        self.filename = None

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create the GUI
        self.create_gui()

    def on_closing(self):
        # Ask the user to confirm whether to close the window or not
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Destroy
            self.window.destroy()
        
    def create_gui(self):
        canvas = Canvas(
            self.window,
            bg = "#FFFFFF",
            height = 600,
            width = 1080,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        canvas.place(x = 0, y = 0)

        background_img = PhotoImage(file = f"assets/background.png")
        background = canvas.create_image(
            540.0, 300.0,
            image=background_img)

        img0 = PhotoImage(file = f"assets/img0.png")
        self.b0 = Button(
            image = img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.open_file,
            relief = "flat")

        self.b0.place(
            x = 69, y = 151,
            width = 150,
            height = 53)

        img1 = PhotoImage(file = f"assets/img1.png")
        self.b1 = Button(
            image = img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.check_draw_graph,
            relief = "flat")

        self.b1.place(
            x = 155, y = 425,
            width = 150,
            height = 53)

        img2 = PhotoImage(file = f"assets/img2.png")
        self.b2 = Button(
            image = img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.check_bonus,
            relief = "flat")

        self.b2.place(
            x = 156, y = 485,
            width = 150,
            height = 53)

        entry0_img = PhotoImage(file = f"assets/img_textBox0.png")
        entry0_bg = canvas.create_image(
            315.0, 178.0,
            image = entry0_img)

        self.entry0 = Entry(
            bd = 0,
            bg = "#a5c9ca",
            highlightthickness = 0,
            font = ("Poppins", 12),
            fg = "#FFFFFF")

        self.entry0.place(
            x = 265.0, y = 156,
            width = 100.0,
            height = 42)

        self.entry0.bind('<Button-1>', lambda e: 'break')

        entry1_img = PhotoImage(file = f"assets/img_textBox1.png")
        entry1_bg = canvas.create_image(
            649.0, 546.0,
            image = entry1_img)

        self.entry1 = Entry(
            bd = 0,
            bg = "#a5c9ca",
            highlightthickness = 0,
            font = ("Poppins", 12),
            fg = "#FFFFFF")

        self.entry1.place(
            x = 604.0, y = 526,
            width = 90.0,
            height = 38)

        self.entry1.bind('<Button-1>', lambda e: 'break')

        entry2_img = PhotoImage(file = f"assets/img_textBox2.png")
        entry2_bg = canvas.create_image(
            917.0, 546.0,
            image = entry2_img)

        self.entry2 = Entry(
            bd = 0,
            bg = "#a5c9ca",
            highlightthickness = 0,
            font = ("Poppins", 12),
            fg = "#FFFFFF")

        self.entry2.place(
            x = 842.0, y = 526,
            width = 150.0,
            height = 38)

        # Combo Box
        self.combobox0 = customtkinter.CTkComboBox(master=self.window,
                                     values=[],
                                     command=self.combobox_start,
                                     bg_color="#E7F6F2",
                                     fg_color="#395B64",
                                     border_color="#395B64",
                                     button_color="#2C3333",
                                     button_hover_color="#464D4D",
                                     dropdown_fg_color="#395B64",
                                     dropdown_hover_color="#2C3333",
                                     font=("Poppins", 14),
                                     dropdown_font=("Poppins", 14),
                                     state="disabled")

        self.combobox0.place(
            x = 215, y = 220,
            )

        self.combobox0.set("")  # set initial value

        self.combobox1 = customtkinter.CTkComboBox(master=self.window,
                                     values=[],
                                     command=self.combobox_target,
                                     bg_color="#E7F6F2",
                                     fg_color="#395B64",
                                     border_color="#395B64",
                                     button_color="#2C3333",
                                     button_hover_color="#464D4D",
                                     dropdown_fg_color="#395B64",
                                     dropdown_hover_color="#2C3333",
                                     font=("Poppins", 14),
                                     dropdown_font=("Poppins", 14),
                                     state="disabled")

        self.combobox1.place(
            x = 215, y = 272,
            )

        self.combobox1.set("")  # set initial value

        self.radio_var = IntVar()

        radiobutton_1 = customtkinter.CTkRadioButton(master=self.window, text="Uniform Cost Search",
                                                     command=self.radiobutton_event, variable= self.radio_var, value=1,
                                                     bg_color="#E7F6F2", 
                                                     text_color="#2C3333", 
                                                     font=("Poppins", 16),
                                                     fg_color="#395B64")

        radiobutton_2 = customtkinter.CTkRadioButton(master=self.window, text="A-Star",
                                                     command=self.radiobutton_event, variable= self.radio_var, value=2,
                                                     bg_color="#E7F6F2", 
                                                     text_color="#2C3333", 
                                                     font=("Poppins", 16),
                                                     fg_color="#395B64")

        radiobutton_1.place(
            x = 190, y = 328,
            )

        radiobutton_2.place(
            x = 190, y = 360,
            )

        # Create canvas for matplotlib graph
        self.setup_plot()

        self.window.mainloop()        

    def combobox_start(self, choice):
        self.start_node = choice

    def combobox_target(self, choice):
        self.target_node = choice

    def radiobutton_event(self):
        self.algorithm_used = self.radio_var.get()
        
    def open_file(self):
        # Open the file dialog to select a file
        self.filename = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )

        self.entry0.delete(0, END)
        self.entry0.insert(0, str(os.path.basename(self.filename)))

        self.check_file()

    def check_file(self):
        with open(self.filename) as f:
            lines = f.readlines()

        num_rows = len(lines) - 2
        num_cols = len(lines[0].split())

        for line in lines:
            if len(line.split()) != num_rows:
                messagebox.showerror("File Out of Format", "Your txt file is out of format, check again!")
                self.entry0.delete(0, END)
                return

        # File format is proved
        # Set combobox
        node_names = lines[-2].split()

        self.combobox0.configure(state="normal", values=node_names)
        self.combobox1.configure(state="normal", values=node_names)

        # Create new graph
        self.G = nx.DiGraph()

        num_nodes = len(lines) - 2 # exclude last 2 line (node_names, coords)
        self.G.add_nodes_from(range(num_nodes))

        points = []
        for point in lines[-1].split():
            x, y = map(float, point.strip("()").split(","))
            points.append((x, y))

        for i in range(num_nodes):
            inp = lines[i].split()
            for j in range(num_nodes):
                if inp[j] != 'inf' and inp[j] != '0':
                    weight = self.get_distance(points[i], points[j])
                    self.G.add_edge(i, j, weight=weight)
        
        # Get node names
        node_labels = {i: name for i, name in enumerate(node_names)}
        self.G = nx.relabel_nodes(self.G, node_labels)    

        plt.clf()
        self.pos = nx.spring_layout(self.G)

        # Loop through nodes and get their positions
        count = 0
        self.node_coords = {}
        for node in self.G.nodes():
            print(node)
            self.node_coords[node] = points[count]
            count += 1

        nx.draw_networkx_nodes(self.G, self.pos, node_color='#1f78b4')
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.G.edges(), edge_color='lightgray')
        nx.draw_networkx_labels(self.G, self.pos, font_size=8)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels={(u, v): f"{w:.3f} km" for (u, v, w) in self.G.edges(data='weight')}, font_size=8)
        
        self.display_graph()

    def display_graph(self):
        # Display matplotlib graph into canvas
        if (hasattr(self, "fig")):
            self.fig = plt.gcf()
            self.canvas_plot.draw()
        else:
            self.fig = plt.gcf()
            self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.canvas_plot)
            self.canvas_plot.draw()

        self.canvas_plot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas_plot.get_tk_widget().configure(width=560, height=400)

    def check_draw_graph(self):
        # Check filename
        if self.filename == None and self.bonus == False:
            messagebox.showwarning("No File Input", "You have to input txt file first!")
            return   

        # Check start_node and target_node
        if not hasattr(self, 'start_node') or not hasattr(self, 'target_node'):
            messagebox.showwarning("No Start/ End Node", "You have to input start node and end node!")
            return  

        # Check algorithm_used
        if not hasattr(self, 'algorithm_used'):
            messagebox.showwarning("No Algorithm Input", "You have to select the algorithm first!")
            return

        if (self.bonus):
            shortest_path = self.get_shortest_path()

            if (shortest_path == -1):
                return

            total_weight = 0
            # Update graph
            for i in range(len(shortest_path)-1):
                path = self.map_widget.set_path([self.node_coords[shortest_path[i]], self.node_coords[shortest_path[i + 1]]], color = "green")
                total_weight += self.get_distance(self.node_coords[shortest_path[i]], self.node_coords[shortest_path[i + 1]])

            # Display Cost
            self.entry1.delete(0, END)
            self.entry1.insert(0, str(round(total_weight, 5)) + " km")

            # Display Route
            path_str = ' → '.join(shortest_path)
            self.entry2.delete(0, END)
            self.entry2.insert(0, str(path_str))

        else:
            self.draw_graph()

    def get_distance(self, coord1, coord2):
        # Approximate radius of earth in km
        R = 6373.0

        lat1, lon1 = coord1
        lat2, lon2 = coord2

        # Convert coordinates to radians
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        # Calculate the difference between the coordinates
        delta_lon = lon2 - lon1
        delta_lat = lat2 - lat1

        # Apply the haversine formula
        a = sin(delta_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Calculate the distance in kilometers
        distance = R * c

        return distance

    def get_shortest_path(self):
        # Get the shortest path between the start and end nodes
        # UCS
        if (self.algorithm_used == 1):
            try:
                shortest_path = UCS.UCS(self.G, self.start_node, self.target_node)
                return shortest_path
            except nx.NetworkXNoPath:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
                return -1
            except ValueError:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
                return -1
        # A-Star
        else:
            try:
                shortest_path = ASTAR.ASTAR(self.G, self.start_node, self.target_node, self.node_coords)
                return shortest_path
            except nx.NetworkXNoPath:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
                return -1
            except ValueError:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
                return -1
        
    def draw_graph(self):
        # Read adjacency matrix from file
        with open(self.filename) as f:
            lines = f.readlines()

        shortest_path = self.get_shortest_path()

        if (shortest_path == -1):
            return

        # Add path edges
        path_edges = [(u, v) for u, v in zip(shortest_path, shortest_path[1:])]

        # Clear
        plt.clf()

        # Update the graph
        node_color = ['red' if node in shortest_path else '#1f78b4' for node in self.G.nodes()]
        nx.draw_networkx_nodes(self.G, self.pos, node_color=node_color)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.G.edges(), edge_color='lightgray')
        nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges, edge_color='r')
        nx.draw_networkx_labels(self.G, self.pos, font_size=8)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels={(u, v): f"{w:.3f} km" for (u, v, w) in self.G.edges(data='weight')}, font_size=8)

        # Display Cost
        shortest_path_weights = [self.G[u][v]['weight'] for u, v in path_edges]
        total_weight = sum(shortest_path_weights)

        self.entry1.delete(0, END)
        self.entry1.insert(0, str(round(total_weight, 5)) + " km")

        # Display Route
        path_str = ' → '.join(shortest_path)
        self.entry2.delete(0, END)
        self.entry2.insert(0, str(path_str))
        
        self.display_graph()

    def setup_plot(self):
        self.canvas_plot = Canvas(self.window, width=560, height=400, bg='#A5C9CA', highlightthickness=0, borderwidth=0)
        self.canvas_plot.place(
            x = 452, y = 110,
            )

    def check_bonus(self):
        if (self.bonus):
            self.canvas_temp.destroy()
            self.setup_plot()
            self.bonus = False
        else:
            self.setup_map_view()

    def setup_map_view(self):
        self.bonus = True
        self.G = nx.Graph()
        self.canvas_temp = Canvas(self.window, width=560, height=400, bg='#E7F6F2', highlightthickness=0, borderwidth=0)
        self.canvas_temp.place(
            x = 452, y = 110,
            )

        # Create map widget
        self.map_widget = TkinterMapView(self.canvas_temp, width=560, height=380, corner_radius=0)
        self.map_widget.place(
            x = 0, y = 35,
            )

        self.entry_search = customtkinter.CTkEntry(master=self.canvas_temp,
                                            placeholder_text="type address ...",
                                            width=200,
                                            font=("Poppins", 14))

        self.entry_search.place(
            x = 0, y = 0
            )

        self.entry_search.bind("<Return>", self.search_event)

        self.button_search = customtkinter.CTkButton(master=self.canvas_temp,
                                                    text="Search",
                                                    width=90,
                                                    command=self.search_event,
                                                    fg_color="#395B64",
                                                    hover_color="#53757E",
                                                    font=("Poppins", 14))

        self.button_search.place(
            x = 210, y = 0
            )

        self.map_option_menu = customtkinter.CTkOptionMenu(self.canvas_temp, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                             command=self.change_map,
                                                                             bg_color="#E7F6F2",
                                                                             fg_color="#395B64",
                                                                             button_color="#2C3333",
                                                                             button_hover_color="#464D4D",
                                                                             dropdown_fg_color="#395B64",
                                                                             dropdown_hover_color="#2C3333",
                                                                             font=("Poppins", 14),
                                                                             dropdown_font=("Poppins", 14)
                                                                             )

        self.map_option_menu.place(
            x = 310, y = 0
            )

        self.button_clear = customtkinter.CTkButton(master=self.canvas_temp,
                                                    text="Clear Marker",
                                                    width=100,
                                                    command=self.clear_marker_event,
                                                    fg_color="#395B64",
                                                    hover_color="#53757E",
                                                    font=("Poppins", 14))

        self.button_clear.place(
            x = 460, y = 0
            )

        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                    command=self.add_marker_event,
                                                    pass_coords=True)

        self.map_widget.add_right_click_menu_command(label="Toggle Pathmaking",
                                                    command=self.enable_path,
                                                    pass_coords=False)

        # Set default values
        self.map_widget.set_address("ITB, Bandung")
        self.map_widget.set_zoom(17)

    def add_marker_event(self, coords):
        print("Add marker:", coords)
        self.countMarker += 1
        node_name = str(self.countMarker)
        new_marker = self.map_widget.set_marker(coords[0], coords[1], text=str(self.countMarker), command=self.marker_clicked)
        self.G.add_node(node_name)
        self.node_coords[node_name]=coords

        marker_list = [str(i) for i in range(1, self.countMarker+1)]

        self.combobox0.configure(state="normal", values=marker_list)
        self.combobox1.configure(state="normal", values=marker_list)

    # Function triggered when a marker is clicked
    def marker_clicked(self, marker):
        if self.is_path_enabled:
            if not self.is_coordinate_saved:
                self.savedcoordinates = marker.position
                self.is_coordinate_saved = True
            else:
                if marker.position != self.savedcoordinates:
                    c1 = marker.position
                    c2 = self.savedcoordinates
                    path = self.map_widget.set_path([c1, c2])
                    self.G.add_edge(self.getKey(c1), self.getKey(c2), weight=geodesic(c1,c2).km)
                    self.is_coordinate_saved = False

    # Enable pathmatking option when right click
    def enable_path(self):
        self.is_path_enabled = not self.is_path_enabled

    # Get a node index given a coordinate
    def getKey(self, coordinate):
        for key in self.node_coords:
            if self.node_coords[key] == coordinate:
                return key
        return -1

    def clear_marker_event(self):
        self.map_widget.delete_all_marker()
        self.countMarker = 0

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry_search.get())

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

# Run App
if __name__ == "__main__":
    app = GraphVisualizer()