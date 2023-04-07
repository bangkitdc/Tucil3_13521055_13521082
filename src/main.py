import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas = None
        self.G = None
        self.filename = None

        # Create the GUI
        self.create_gui()
        
    def create_gui(self):
        # Frame
        frame = tk.Frame(self.root)
        frame.pack(side=tk.TOP, pady=10)

        # Open button
        open_button = tk.Button(frame, text="Open", command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=10)

        # Draw button
        draw_button = tk.Button(frame, text="Draw", command=self.draw_graph)
        draw_button.pack(side=tk.LEFT, padx=10)
        
        # Start entry
        start_label = tk.Label(frame, text="Start:")
        start_label.pack(side=tk.LEFT, padx=10)
        self.start_entry = tk.Entry(frame, width=5)
        self.start_entry.pack(side=tk.LEFT)

        # End entry
        end_label = tk.Label(frame, text="End:")
        end_label.pack(side=tk.LEFT, padx=10)
        self.end_entry = tk.Entry(frame, width=5)
        self.end_entry.pack(side=tk.LEFT)

        # Create canvas for matplotlib graph
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack(side=tk.TOP, padx=10, pady=10)
        
        # Create label for total weight
        self.weight_label = tk.Label(self.root, text="Total weight: ")
        self.weight_label.pack(side=tk.BOTTOM, padx=10, pady=10)
        
    def open_file(self):
        # Open the file dialog to select a file
        self.filename = filedialog.askopenfilename()
        
    def draw_graph(self):
        # Read adjacency matrix from file
        with open(self.filename) as f:
            lines = f.readlines()

        # Create new graph
        G = nx.Graph()

        num_nodes = len(lines) - 1 # exclude last line (node_names)
        G.add_nodes_from(range(num_nodes))

        for i in range(num_nodes):
            weights = lines[i].split()
            for j in range(num_nodes):
                if weights[j] != 'inf':
                    weight = int(weights[j])
                    G.add_edge(i, j, weight=weight)
        
        # Todo: VALIDASI FILE SEMUANYA
        
        node_names = lines[-1].split()
        node_labels = {i: name for i, name in enumerate(node_names)}
        G = nx.relabel_nodes(G, node_labels)
                    
        # Get the start and end nodes from the user input
        if len(self.start_entry.get()) != 0 and len(self.end_entry.get()) != 0:
            start_node = self.start_entry.get()
            end_node = self.end_entry.get()
        else:
            messagebox.showwarning("No Start/ End Node", "You have to input start node and end node!")
            return
        
        # Get the shortest path between the start and end nodes
        # Todo: THE ALGORITHMS
        try:
            shortest_path = nx.shortest_path(G, start_node, end_node, weight='weight')
        except nx.NetworkXNoPath:
            messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
            return
        
        # Draw the graph on canvas
        pos = nx.spring_layout(G)
        
        node_color = ['red' if node in shortest_path else '#1f78b4' for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_color=node_color)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='lightgray')
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v) for u, v, d in G.edges(data=True) if (u, v) in zip(shortest_path, shortest_path[1:])], edge_color='r', width=2)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
        
        shortest_path_weights = [G[u][v]['weight'] for u, v in zip(shortest_path, shortest_path[1:])]
        total_weight = sum(shortest_path_weights)
        self.weight_label.config(text=f"Total weight: {total_weight}")
        
        # Display matplotlib graph into canvas
        fig = plt.gcf()
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
                                        
    def run(self):
        self.root.mainloop()

# Run App
app = GraphVisualizer()
app.run()