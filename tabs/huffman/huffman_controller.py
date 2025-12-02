"""Controller: Handles user interactions for Huffman tab"""
import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
from app_theme.dark_theme import ModernDarkTheme


class HuffmanController:
    """Coordinates between HuffmanModel and HuffmanView"""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._bind_commands()

    def _bind_commands(self):
        """Connect buttons to handlers"""
        self.view.analyze_btn.config(command=self.handle_analyze_with_probs)
        self.view.tree_btn.config(command=self.handle_build_tree_visual)
        self.view.analyze_text_btn.config(command=self.handle_analyze_text_huffman)

    def handle_analyze_with_probs(self):
        """Your original analyze function"""
        try:
            pairs = self.view.code_dictionary.get("1.0", tk.END).split()
            code_dict = {s: c.strip() for s, c in (p.split(":") for p in pairs if ":" in p)}

            prob_pairs = self.view.prob_text.get("1.0", tk.END).split()
            prob_dict = {s: float(p) for s, p in (p.split(":") for p in prob_pairs if ":" in p)}

            if set(code_dict.keys()) != set(prob_dict.keys()):
                raise ValueError("Τα σύμβολα στον κώδικα και τις πιθανότητες πρέπει να ταιριάζουν!")

            if not np.isclose(sum(prob_dict.values()), 1.0, atol=0.0001):
                messagebox.showwarning("Προσοχή",f"Οι πιθανότητες αθροίζουν σε {sum(prob_dict.values()):.4f}, όχι σε 1.0!!!")

            avg_length = self.model.calculate_avrg_length(code_dict, prob_dict)
            shannon_h = self.model.calculate_entropy_from_dictionary(prob_dict)
            non_sing = self.model.is_non_singular(code_dict)
            instant = self.model.is_instantaneous(code_dict)
            kraft_sum, kraft_ok = self.model.kraft_inequality(code_dict)

            self.view.res5.delete("1.0", tk.END)
            self.view.res5.insert(tk.END, "--- Αποτελέσματα ---\n")
            self.view.res5.insert(tk.END, f"Ευκρινής (Non-singular): {non_sing}\n")
            self.view.res5.insert(tk.END, f"Στιγμιαία αποκωδικοποιήσιμος (Prefix-free): {instant}\n")
            self.view.res5.insert(tk.END, f"Kraft Sum: {kraft_sum:.6f}\n")
            self.view.res5.insert(tk.END, f"Ικανοποιεί την ανισότητα Kraft : {kraft_ok}\n\n")
            self.view.res5.insert(tk.END, f"Μέσο Μήκος Κώδικα (L): {avg_length:.4f} bits/symbol\n")
            self.view.res5.insert(tk.END, f"Εντροπία (H): {shannon_h:.4f} bits/symbol\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_build_tree_visual(self):
        """Your original tree visualization"""
        try:
            pairs = self.view.code_dictionary.get("1.0", tk.END).split()
            code_dict = {s: c.strip() for s, c in (p.split(":") for p in pairs if ":" in p)}

            if not code_dict:
                raise ValueError("Παρακαλώ εισάγετε έγκυρο κώδικα!")

            tree = self.view.build_tree_graph(code_dict)
            pos = self.view.hierarchy_pos(tree, "root", width=2.0, vert_gap=0.2, vert_loc=0)

            self.view.ax5.clear()
            self.view.ax5.set_facecolor(ModernDarkTheme.BG_FRAME)
            self.view.ax5.axis('off')

            nx.draw_networkx_nodes(tree, pos, node_color='#76C7C0',node_size=1800, alpha=0.8, ax=self.view.ax5)
            nx.draw_networkx_edges(tree, pos, edge_color='#A8DADC',arrows=True, arrowsize=15, width=2, ax=self.view.ax5)
            edge_labels = nx.get_edge_attributes(tree, 'label')
            nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels,font_size=11, font_color="black",ax=self.view.ax5)

            node_labels = {}
            for node_name, attributes in tree.nodes(data=True):
                if 'label' in attributes:
                    symbol = attributes['label']
                    codeword = code_dict.get(symbol, "N/A")
                    node_labels[node_name] = f"{symbol}\n{codeword}"
                elif node_name == "root":
                    node_labels[node_name] = "ROOT"
                else:
                    node_labels[node_name] = ""

            nx.draw_networkx_labels(tree, pos, node_labels,font_size=10, font_weight='bold',font_color='#1E222A', ax=self.view.ax5)

            self.view.ax5.set_title("Δέντρο Κωδικών Λέξεων",color=ModernDarkTheme.WHITE_TEXT, fontsize=14, pad=20)

            self.view.canvas5.draw()

            self.view.res5.insert(tk.END, "\n--- Πληροφορίες Δέντρου ---\n")
            self.view.res5.insert(tk.END, f"Αριθμός κόμβων: {tree.number_of_nodes()}\n")
            self.view.res5.insert(tk.END, f"Αριθμός ακμών: {tree.number_of_edges()}\n")
            self.view.res5.insert(tk.END, f"Μέγιστο βάθος: {max(len(code) for code in code_dict.values())}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_analyze_text_huffman(self):
        """Generate Huffman codes from text"""
        try:
            text = self.view.text_input.get("1.0", tk.END).strip()
            if not text:
                messagebox.showerror("Σφάλμα", "Εισάγετε κείμενο!")
                return

            codes, probs, freq = self.model.generate_huffman_codes(text)

            H = self.model.calculate_entropy_from_dictionary(probs)
            L = sum(probs[c] * len(codes[c]) for c in codes)

            self.view.text_result.delete("1.0", tk.END)
            self.view.text_result.insert(tk.END, "Ανάλυση Huffman\n")
            self.view.text_result.insert(tk.END, f"Χαρακτήρες: {len(text)}\n")
            self.view.text_result.insert(tk.END, f"Μοναδικοί: {len(freq)}\n\n")
            self.view.text_result.insert(tk.END, f"Εντροπία H: {H:.4f} bits\n")
            self.view.text_result.insert(tk.END, f"Μέσο Μήκος L: {L:.4f} bits\n")
            self.view.text_result.insert(tk.END, "Κώδικες Huffman:\n")

            for char, code in sorted(codes.items(), key=lambda x: len(x[1])):
                c = repr(char)[1:-1] if char not in [' ', '\n'] else ('SP' if char == ' ' else 'NL')
                self.view.text_result.insert(tk.END, f"'{c}' → {code} ({freq[char]} φορές)\n")

        except Exception as e:
            messagebox.showerror("Σφάλμα", str(e))
