"""Base view class with common widget creation methods"""
import tkinter as tk
from tkinter import scrolledtext
from app_theme.dark_theme import ModernDarkTheme


class SharedUI:
    """Base class for all tab views with common widget helpers"""

    def _label(self, parent, text, row, col, **grid):
        """Create and grid a label"""
        lbl = tk.Label(parent, text=text, bg=ModernDarkTheme.BG_FRAME,
                       fg=ModernDarkTheme.WHITE_TEXT, font=("Consolas", 11))
        lbl.grid(row=row, column=col, sticky="w", padx=6, pady=4, **grid)
        return lbl

    def _scrolled(self, parent, h=12,default=""):
        """Create a scrolled text widget
        :param default:
        """
        txt = scrolledtext.ScrolledText(parent, height=h, bg="#1E222A",
                                        fg=ModernDarkTheme.WHITE_TEXT,
                                        insertbackground=ModernDarkTheme.WHITE_TEXT,
                                        font=("Consolas", 16))
        txt.insert("1.0",default)
        return txt

    def _button(self, parent, text, color=None, cmd=None):
        """
        Create a styled button (not gridded)

        Args:
            parent: Parent widget
            text: Button text
            color: Background color (defaults to BG_BLUISH)
            cmd: Command callback

        Returns:
            Configured Button widget
        """
        if color is None:
            color = ModernDarkTheme.BG_BLUISH
        btn = tk.Button(parent, text=text, command=cmd,
                        bg=color, fg="#FFFFFF",
                        font=("Consolas", 11, "bold"))
        return btn

    def _entry(self, parent, width=10, default=""):
        """
        Create a styled entry widget (not gridded)

        Args:
            parent: Parent widget
            width: Entry width in characters
            default: Default text to insert

        Returns:
            Configured Entry widget
        """
        entry = tk.Entry(parent, width=width,
                         bg=ModernDarkTheme.BG_ENTRY,
                         fg=ModernDarkTheme.WHITE_TEXT,
                         insertbackground=ModernDarkTheme.WHITE_TEXT,
                         font=("Consolas", 11))
        if default:
            entry.insert(0, default)
        return entry