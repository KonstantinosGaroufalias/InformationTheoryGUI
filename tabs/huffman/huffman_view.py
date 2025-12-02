"""View: GUI components for Huffman tab"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx
from app_theme.dark_theme import ModernDarkTheme
from tabs.common.shared_ui import SharedUI

class HuffmanView(SharedUI):
    """Manages all GUI components for Huffman coding"""

    def __init__(self, parent_notebook):
        self.parent_notebook = parent_notebook

        # Create main frame for this tab
        self.frame = tk.Frame(parent_notebook, bg=ModernDarkTheme.BG_FRAME)
        parent_notebook.add(self.frame, text="Ανάλυση Κώδικα και Δένδρο huffman")

        # Create sub-notebook
        self.lab5_notebook = ttk.Notebook(self.frame)
        self.lab5_notebook.pack(expand=True, fill="both")

        # Create subtabs
        self._create_manual_code_subtab()
        self._create_text_analysis_subtab()

    def _create_manual_code_subtab(self):
        """Your existing manual code analysis"""
        f = tk.Frame(self.lab5_notebook, bg=ModernDarkTheme.BG_FRAME)
        self.lab5_notebook.add(f, text="Ανάλυση Κώδικα")

        # LEFT SIDE: Code Dictionary Input
        leftframe = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        leftframe.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        self._label(leftframe, "Λεξικό Κώδικα:", 0, 0)
        self._label(leftframe, "(Σε μορφή: A:110 B:01 C:00 D:10)", 1, 0)

        self.code_dictionary = scrolledtext.ScrolledText(leftframe, height=8, width=30,
                                                        bg=ModernDarkTheme.BG_ENTRY, fg=ModernDarkTheme.WHITE_TEXT,
                                                        insertbackground=ModernDarkTheme.WHITE_TEXT,
                                                        font=("Consolas", 14))
        self.code_dictionary.insert(tk.END, "A:110 B:01 C:00 D:10")
        self.code_dictionary.grid(row=2, column=0, padx=6, pady=4, sticky="nsew")

        # RIGHT SIDE: Probabilities Input
        right_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        right_frame.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

        self._label(right_frame, "Πιθανότητες:", 0, 0)
        self._label(right_frame, "(Σε μορφή: A:0.25 B:0.25 C:0.25 D:0.25)", 1, 0)

        self.prob_text = scrolledtext.ScrolledText(right_frame, height=8, width=30,
                                                   bg=ModernDarkTheme.BG_ENTRY, fg=ModernDarkTheme.WHITE_TEXT,
                                                   insertbackground=ModernDarkTheme.WHITE_TEXT,
                                                   font=("Consolas", 14))
        self.prob_text.insert(tk.END, "A:0.25 B:0.25 C:0.25 D:0.25")
        self.prob_text.grid(row=2, column=0, padx=6, pady=4, sticky="nsew")

        leftframe.grid_rowconfigure(2, weight=1)
        leftframe.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Buttons row below both inputs
        button_frame = tk.Frame(f, bg=ModernDarkTheme.BG_FRAME)
        button_frame.grid(row=1, column=0, columnspan=2, pady=6)

        # CHANGED: Replaced tk.Button with self._button
        self.analyze_btn = self._button(button_frame, "Ανάλυση Κώδικα",
                                        color=ModernDarkTheme.BG_BLUISH)
        self.analyze_btn.grid(row=0, column=0, padx=6, pady=4)

        # CHANGED: Replaced tk.Button with self._button
        self.tree_btn = self._button(button_frame, "Προβολή Δένδρου huffman",
                                     color=ModernDarkTheme.BG_LIGHT_ORANGE)
        self.tree_btn.grid(row=0, column=1, padx=6, pady=4)

        # Results text (smaller now)
        self.res5 = self._scrolled(f, 12)
        self.res5.grid(row=2, column=0, columnspan=2, padx=6, pady=6, sticky="ew")

        # Matplotlib figure (BIGGER)
        self.fig5 = Figure(figsize=(10, 8), dpi=90, facecolor=ModernDarkTheme.BG_FRAME)
        self.ax5 = self.fig5.add_subplot(111, facecolor=ModernDarkTheme.BG_FRAME)
        self.ax5.axis('off')

        self.canvas5 = FigureCanvasTkAgg(self.fig5, f)
        self.canvas5.get_tk_widget().grid(row=3, column=0, columnspan=2,
                                         padx=6, pady=6, sticky="nsew")

        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=1)
        f.grid_rowconfigure(0, weight=0)
        f.grid_rowconfigure(2, weight=0)
        f.grid_rowconfigure(3, weight=1)

    def _create_text_analysis_subtab(self):
        """NEW: Text to Huffman codes"""
        f = tk.Frame(self.lab5_notebook, bg=ModernDarkTheme.BG_FRAME)
        self.lab5_notebook.add(f, text="Ανάλυση Κειμένου")

        tk.Label(f, text="Εισάγετε κείμενο για Huffman:",
                bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                font=("Consolas", 12, "bold")).pack(pady=10)

        self.text_input = scrolledtext.ScrolledText(f, height=8,
                                                    bg=ModernDarkTheme.BG_ENTRY,
                                                    fg=ModernDarkTheme.WHITE_TEXT,
                                                    font=("Consolas", 11))
        self.text_input.insert(tk.END,
            "Το μάθημα αποσκοπεί στο να παράσχει στο σπουδαστή βασικές γνώσεις της θεωρίας πληροφοριών και κωδίκων. "
            "Οι γνώσεις αυτές θεωρούνται απαραίτητες για τη μελέτη και ανάλυση τηλεπικοινωνιακών συστημάτων καθώς και "
            "για την κατανόηση τεχνικών κωδικοποίησης δεδομένων.")
        self.text_input.pack(padx=20, pady=5, fill=tk.BOTH)

        # CHANGED: Replaced tk.Button with self._button
        self.analyze_text_btn = self._button(f, "Ανάλυση & Δημιουργία Huffman",color=ModernDarkTheme.BG_BLUISH)
        self.analyze_text_btn.pack(pady=10)

        self.text_result = self._scrolled(f, 18)
        self.text_result.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def build_tree_graph(self, code_dict):
        """Build tree"""
        tree = nx.DiGraph()
        for symbol, code in code_dict.items():
            current_node = "root"
            tree.add_node(current_node)
            for i, bit in enumerate(code):
                next_node = f"{current_node}-{bit}"
                if not tree.has_edge(current_node, next_node):
                    tree.add_edge(current_node, next_node, label=bit)
                current_node = next_node
            tree.nodes[current_node]['label'] = symbol
        return tree

    def hierarchy_pos(self, G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        """Calculate hierarchical tree layout positions"""
        def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0,
                          xcenter=0.5, pos=None, parent=None, parsed=None):
            if parsed is None:
                parsed = []
            if pos is None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)

            children = list(G.neighbors(root))
            if not isinstance(G, nx.DiGraph) and parent is not None:
                children.remove(parent)

            if len(children) != 0:
                dx = width / len(children)
                nextx = xcenter - width / 2 - dx / 2
                for child in children:
                    nextx += dx
                    pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                        vert_loc=vert_loc + vert_gap, xcenter=nextx,
                                        pos=pos, parent=root, parsed=parsed)
            return pos

        return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
