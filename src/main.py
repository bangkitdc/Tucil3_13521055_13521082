import networkx as nx
import matplotlib.pyplot as plt
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import UCS
import ASTAR

def btn_clicked():
    print("Button Clicked")

class GraphVisualizer:
    def __init__(self):
        self.window = Tk()

        self.window.geometry("1080x600")
        self.window.configure(bg = "#FFFFFF")
        self.window.resizable(False, False)

        self.G = None
        self.coords = {}
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
            command = btn_clicked,
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
        self.canvas_plot = Canvas(canvas, width=560, height=400, bg='#A5C9CA')
        self.canvas_plot.place(
            x = 452, y = 110,
            )

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

        num_rows = len(lines) - 1
        num_cols = len(lines[0].split())

        for line in lines:
            if len(line.split()) != num_rows:
                messagebox.showerror("File Out of Format", "Your txt file is out of format, check again!")
                self.entry0.delete(0, END)
                return

        # File format is proved
        # Set combobox
        node_names = lines[-1].split()

        self.combobox0.configure(state="normal", values=node_names)
        self.combobox1.configure(state="normal", values=node_names)

        # Create new graph
        self.G = nx.DiGraph()

        num_nodes = len(lines) - 1 # exclude last line (node_names)
        self.G.add_nodes_from(range(num_nodes))

        for i in range(num_nodes):
            weights = lines[i].split()
            for j in range(num_nodes):
                if weights[j] != 'inf' and weights[j] != '0':
                    weight = int(weights[j])
                    self.G.add_edge(i, j, weight=weight)
        
        # Get node names
        node_labels = {i: name for i, name in enumerate(node_names)}
        self.G = nx.relabel_nodes(self.G, node_labels)    

        plt.clf()
        self.pos = nx.spring_layout(self.G)

        # Loop through nodes and get their positions
        self.coords = {}
        for node in self.G.nodes():
            x, y = self.pos[node]
            self.coords[node] = (float(x), float(y))

        nx.draw_networkx_nodes(self.G, self.pos, node_color='#1f78b4')
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.G.edges(), edge_color='lightgray')
        nx.draw_networkx_labels(self.G, self.pos)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=nx.get_edge_attributes(self.G, 'weight'))
        
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
        if self.filename == None:
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

        self.draw_graph()
        
    def draw_graph(self):
        # Read adjacency matrix from file
        with open(self.filename) as f:
            lines = f.readlines()

        # Get the shortest path between the start and end nodes
        # UCS
        if (self.algorithm_used == 1):
            try:
                shortest_path = UCS.UCS(self.G, self.start_node, self.target_node)
            except nx.NetworkXNoPath:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
                return
            except ValueError:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
        # A-Star
        else:
            try:
                shortest_path = ASTAR.ASTAR(self.G, self.start_node, self.target_node, self.coords)
            except nx.NetworkXNoPath:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
                return
            except ValueError:
                messagebox.showwarning("No Path Found", "There is no path between the start and end nodes.")
        
        # Update the graph
        path_edges = [(u, v) for u, v in zip(shortest_path, shortest_path[1:])]

        # Clear
        plt.clf()
        
        node_color = ['red' if node in shortest_path else '#1f78b4' for node in self.G.nodes()]
        nx.draw_networkx_nodes(self.G, self.pos, node_color=node_color)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=self.G.edges(), edge_color='lightgray')
        nx.draw_networkx_edges(self.G, self.pos, edgelist=path_edges, edge_color='r')
        nx.draw_networkx_labels(self.G, self.pos)
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=nx.get_edge_attributes(self.G, 'weight'))

        # Display Cost
        shortest_path_weights = [self.G[u][v]['weight'] for u, v in path_edges]
        total_weight = sum(shortest_path_weights)

        self.entry1.delete(0, END)
        self.entry1.insert(0, str(total_weight))

        # Display Route
        path_str = ' -> '.join(shortest_path)
        self.entry2.delete(0, END)
        self.entry2.insert(0, str(path_str))
        
        self.display_graph()

# Run App
if __name__ == "__main__":
    app = GraphVisualizer()