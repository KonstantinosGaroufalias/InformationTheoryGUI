"""
Module που περιέχει την κλάση SharedUI που κληρωνομούν όλες οι main, huffman_view, channel_view και entropy_view
"""

import tkinter as tk
from tkinter import scrolledtext  # Widget κειμένου με scrollbar
from app_theme.dark_theme import ModernDarkTheme

class SharedUI:
    """
    Η βασική κλάση.
    Παρέχει κοινές μεθόδους για τη δημιουργία UI αντικειμένων σε όλη την εφαρμογή.
    """

    def _label(self, parent, text, row, col):
        """
        Δημιουργεί την ετικέτα (Label) χρησιμοποιείται για στατικό κείμενο.

        Παράμετροι:
            parent: Γονικό widget (container)
            text: Κείμενο προς εμφάνιση
            row: Γραμμή στο grid layout
            col: Στήλη στο grid layout
        """
        lbl = tk.Label(
            parent,
            text=text,
            bg=ModernDarkTheme.BG_FRAME,  # Χρώμα φόντου
            fg=ModernDarkTheme.WHITE_TEXT,  # Λευκό χρώμα κειμένου
            font=("Consolas", 11)
        )
        # Τοποθέτηση με grid manager
        lbl.grid(row=row, column=col, sticky="w", padx=6, pady=4)
        return lbl

    def _scrolled(self, parent, h=12, default=""):
        """""
        Χρησιμοποιείται για την εμφάνιση των αποτελεσμάτων πράξεων.

        Παράμετροι:
            parent: Γονικό widget
            h: Ύψος σε γραμμές κειμένου
            default: Προεπιλεγμένο κείμενο κατά την αρχικοποίηση
        """
        txt = scrolledtext.ScrolledText(
            parent,
            height=h,
            bg="#1E222A",
            fg=ModernDarkTheme.WHITE_TEXT,
            insertbackground=ModernDarkTheme.WHITE_TEXT,
            font=("Consolas", 16)
        )
        txt.insert("1.0", default)
        return txt

    def _button(self, parent, text, color=None, cmd=None):
        """
        Δημιουργεί ένα κουμπί (Button).

        Τα κουμπιά είναι τα κύρια στοιχεία αλληλεπίδρασης για την εκτέλεση
        εντολών . Κάθε κουμπί συνδέεται με μια συνάρτηση που εκτελείται κατά το πάτημα.

        Παράμετροι:
            parent: Γονικό widget
            text: Κείμενο
            color: Χρώμα φόντου (προεπιλογή: γαλάζιο)
            cmd: Συνάρτηση
        """
        # Εάν δεν δοθεί χρώμα, χρήση BG_BLUISH
        if color is None:
            color = ModernDarkTheme.BG_BLUISH

        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            bg=color,
            fg=ModernDarkTheme.WHITE_TEXT,
            font=("Consolas", 11, "bold")
        )
        return btn

    def _entry(self, parent, width=10, default=""):
        """
        Δημιουργεί ένα παράθυρο εισαγωγής κειμένου.

        Τα Entry χρησιμοποιούνται για την είσοδο κειμένου από τον χρήστη

        Παράμετροι:
            parent: Γονικό widget
            width: Πλάτος σε χαρακτήρες
            default: Προεπιλεγμένο κείμενο
        """
        entry = tk.Entry(
            parent,
            width=width,  # Πλάτος σε χαρακτήρες όχι pixels
            bg=ModernDarkTheme.BG_ENTRY,
            fg=ModernDarkTheme.WHITE_TEXT,
            insertbackground=ModernDarkTheme.WHITE_TEXT,  # Δρομέας κειμένου
            font=("Consolas", 11)
        )
        # Εισαγωγή προεπιλεγμένου κειμένου εάν παρέχεται
        if default:
            entry.insert(0, default)  # Θέση 0 = αρχή του πεδίου
        return entry
