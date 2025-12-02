"""Main application entry point - MVC Orchestrator"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from app_theme.dark_theme import ModernDarkTheme
from tabs.common.shared_ui import SharedUI

# Import tab components
from tabs.entropy import EntropyModel, EntropyView, EntropyController
from tabs.channel import ChannelModel, ChannelView, ChannelController
from tabs.huffman import HuffmanModel, HuffmanView, HuffmanController

class InfoTheoryApp(SharedUI):  # CHANGED: Inherit from SharedUI
    """Main application class - orchestrates all MVC components"""

    def __init__(self, root):
        self.root = root
        self.root.title("Information-Theory Calculator (Dark) - MVC Edition")
        self.root.geometry("1920x1080")
        self.root.configure(bg=ModernDarkTheme.BG_MAIN)

        # Configure styles
        self._configure_style()

        # Create menu
        self._create_menu_bar()

        # Create main notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Initialize all tab components
        self._init_entropy_tab()
        self._init_channel_tab()
        self._init_huffman_tab()

    def _configure_style(self):
        """Configure ttk styles"""
        style = ttk.Style(self.root)
        style.theme_use("default")
        style.configure("TNotebook", background=ModernDarkTheme.BG_MAIN, borderwidth=0)
        style.configure("TNotebook.Tab", foreground=ModernDarkTheme.WHITE_TEXT,
                       background=ModernDarkTheme.BG_FRAME, padding=(12, 6))
        style.map("TNotebook.Tab", background=[("selected", ModernDarkTheme.BG_BLUISH)])

    def _init_entropy_tab(self):
        """Initialize Entropy tab (MVC)"""
        entropy_model = EntropyModel()
        entropy_view = EntropyView(self.notebook)
        entropy_controller = EntropyController(entropy_model, entropy_view)

    def _init_channel_tab(self):
        """Initialize Channel tab (MVC)"""
        channel_model = ChannelModel()
        channel_view = ChannelView(self.notebook)
        channel_controller = ChannelController(channel_model, channel_view)

    def _init_huffman_tab(self):
        """Initialize Huffman tab (MVC)"""
        huffman_model = HuffmanModel()
        huffman_view = HuffmanView(self.notebook)
        huffman_controller = HuffmanController(huffman_model, huffman_view)

    def _create_menu_bar(self):
        """Create top menu bar"""
        menubar = tk.Menu(self.root, bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT)
        help_menu = tk.Menu(menubar, tearoff=0,bg=ModernDarkTheme.BG_FRAME,fg=ModernDarkTheme.WHITE_TEXT,
                            activebackground=ModernDarkTheme.BG_BLUISH,activeforeground="#FFFFFF")
        help_menu.add_command(label="Οδηγίες Χρήσης",
                             command=self.show_instructions)
        help_menu.add_separator()
        help_menu.add_command(label="Σχετικά με την εφαρμογή",
                             command=self.show_about)
        menubar.add_cascade(label="Βοήθεια", menu=help_menu)
        self.root.config(menu=menubar)

    def show_instructions(self):
        """Display instructions window"""
        self._show_help_window("Οδηγίες Χρήσης", "instructions.txt")

    def show_about(self):
        """Display about window"""
        self._show_help_window("Σχετικά με την εφαρμογή", "about_info.txt")

    def _show_help_window(self, title, filename):
        """Generic help window"""
        help_window = tk.Toplevel(self.root)
        help_window.title(title)
        help_window.geometry("900x700")
        help_window.configure(bg=ModernDarkTheme.BG_MAIN)

        title_label = tk.Label(help_window, text=f"{title}",bg=ModernDarkTheme.BG_MAIN,
                               fg=ModernDarkTheme.BG_BLUISH,font=("Consolas", 16, "bold"))
        title_label.pack(pady=15)

        help_text = self._scrolled(help_window, h=25)
        help_text.config(wrap=tk.WORD, padx=15, pady=10)
        help_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                help_content = f.read()
                help_text.insert("1.0", help_content)
        except FileNotFoundError:
            help_text.insert("1.0", "Το αρχείο δεν βρέθηκε!")

        help_text.config(state=tk.DISABLED)

        close_btn = self._button(help_window, "Κλείσιμο",
                                 color=ModernDarkTheme.BG_LIGHT_ORANGE,
                                 cmd=help_window.destroy)
        close_btn.config(padx=20, pady=5)  # Add padding
        close_btn.pack(pady=10)


def main():
    """Application entry point"""
    root = tk.Tk()
    app = InfoTheoryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
