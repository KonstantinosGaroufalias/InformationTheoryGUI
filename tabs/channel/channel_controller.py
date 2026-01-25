import tkinter as tk
from tkinter import messagebox
from app_theme.dark_theme import ModernDarkTheme
import numpy as np


class ChannelController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self._bind_commands()

    def _bind_commands(self):
        # BSC υποκαρτέλα
        self.view.calc_bsc_btn.config(command=self.handle_calc_bsc)

        # Matrix υποκαρτέλα
        self.view.create_matrix_btn.config(command=self.handle_create_matrix)
        self.view.calc_capacity_btn.config(command=self.handle_calculate_capacity)

        # Chain υποκαρτέλα
        self.view.create_chain_btn.config(command=self.handle_create_chain_matrices)
        self.view.calc_chain_btn.config(command=self.handle_calculate_chain)

    def handle_calc_bsc(self):
        try:
            e = float(self.view.e_entry.get())

            if not 0 <= e <= 1:
                raise ValueError("Το e(bit error rate) πρέπει να ανήκει στο διάστημα 0 έως 1")

            C = self.model.calculate_bsc_capacity(e)

            self.view.bsc_result.delete("1.0", tk.END)
            self.view.bsc_result.insert(tk.END, "Δυαδικό συμμετρικό κανάλη (BSC)\n")
            self.view.bsc_result.insert(tk.END, f"e = {e}\n")
            self.view.bsc_result.insert(tk.END, f"Χωρητικότητα του BSC: C_BSC(e) = {C:.4f} bits/symbol\n")

            # Δημιουργία του plot για BSC
            x_vals, y_vals = self.model.generate_bsc_curve_graphics()

            self.view.ax.clear()

            self.view.ax.set_facecolor(self.view.ax.get_facecolor())

            self.view.ax.plot(x_vals, y_vals, color=ModernDarkTheme.BG_BLUISH, lw=2, label='C_BSC(e)')
            self.view.ax.axvline(e, color=ModernDarkTheme.BG_LIGHT_ORANGE, ls="--", lw=1.5, label=f'e={e}')

            self.view.ax.set_xlabel(" (e)", color=ModernDarkTheme.WHITE_TEXT, fontsize=10)
            self.view.ax.set_ylabel("Χωρητικότητα (bits/symbol)", color=ModernDarkTheme.WHITE_TEXT, fontsize=10)
            self.view.ax.set_title("BSC Graphic", color=ModernDarkTheme.WHITE_TEXT, fontsize=12)

            self.view.ax.legend(facecolor=ModernDarkTheme.BG_FRAME, edgecolor=ModernDarkTheme.WHITE_TEXT,labelcolor=ModernDarkTheme.WHITE_TEXT)
            self.view.ax.grid(True, alpha=0.2, color=ModernDarkTheme.WHITE_TEXT)

            self.view.canvas.draw()

        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα: {str(e)}")

    def handle_create_matrix(self):
        try:
            rows = int(self.view.rows_entry.get())
            cols = int(self.view.cols_entry.get())

            if rows <= 0 or cols <= 0:

                messagebox.showerror("Σφάλμα", "Θα πρέπει να εισάγετε μόνο θετικούς αριθμούς!")

                return

            # Clear matrix
            for widget in self.view.matrix_frame.winfo_children():
                widget.destroy()

            self.view.matrix_entries = []

            # Create header
            tk.Label(self.view.matrix_frame, text="P(Y|X)",bg=ModernDarkTheme.BG_FRAME,
                     fg=ModernDarkTheme.BG_BLUISH,font=("Consolas", 10, "bold")).grid(row=0, column=0, padx=4, pady=4)

            # Column headers
            for j in range(cols):
                tk.Label(self.view.matrix_frame, text=f"Y{j + 1}",bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                         font=("Consolas", 9, "bold")).grid(row=0, column=j + 1, padx=2)

            # Create entry grid
            for i in range(rows):

                # Row header
                tk.Label(self.view.matrix_frame, text=f"X{i + 1}",bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.BG_BLUISH,
                         font=("Consolas", 9, "bold")).grid(row=i + 1, column=0, padx=4)

                row_entries = []
                for j in range(cols):
                    entry = tk.Entry(self.view.matrix_frame, width=7,bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                                     font=("Consolas", 9),justify='center',insertbackground=ModernDarkTheme.WHITE_TEXT)
                    entry.insert(0, f"{1.0 / cols:.2f}")  # Default uniform distribution
                    entry.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                    row_entries.append(entry)

                self.view.matrix_entries.append(row_entries)

            self.view.matrix_result.delete("1.0", tk.END)

            self.view.matrix_result.insert(tk.END, f"Ο Πίνακας {rows}×{cols} δημιουργήθηκε με επιτυχία!\n\n")
            self.view.matrix_result.insert(tk.END, "Σημείωση: Κάθε γραμμή πρέπει να αθροίζει σε 1\n")
            self.view.matrix_result.insert(tk.END, "Πίνακας P(Y|X)\n")

        except ValueError:

            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρους ακέραιους αριθμούς!")

    def handle_calculate_capacity(self):
        try:
            if not self.view.matrix_entries:
                messagebox.showerror("Σφάλμα", "Μη βιάζεστε! Δημιουργήστε πρώτα έναν πίνακα!")
                return
            matrix_data = []
            for i, row in enumerate(self.view.matrix_entries):
                row_values = [float(entry.get()) for entry in row]

                if not self.model.check_for_correct_probabilities(row_values):
                    raise ValueError(f"Γραμμή {i + 1}: Όλες οι τιμές πρέπει να είναι στο [0,1]")

                if not np.isclose(sum(row_values), 1.0, atol=0.01):
                    messagebox.showwarning("Προειδοποίηση",f"Γραμμή {i + 1} αθροίζει σε {sum(row_values):.3f} (όχι 1.0)")

                matrix_data.append(row_values)

            P_YX = np.array(matrix_data)
            m = int(self.view.m_entry.get())

            if m <= 0:
                raise ValueError("Το M πρέπει να είναι θετικός ακέραιος!")

            capacity, x_optimal = self.model.calculate_uniform_channel_capacity(m, P_YX, 1)

            self.view.matrix_result.delete("1.0", tk.END)
            self.view.matrix_result.insert(tk.END, "--- Αποτελέσματα ---\n")
            self.view.matrix_result.insert(tk.END, "\nΧωρητικότητα Διαύλου\n")

            self.view.matrix_result.insert(tk.END, "Πίνακας Καναλιού P(Y|X):\n")
            self.view.matrix_result.insert(tk.END, f"{P_YX}\n\n")

            self.view.matrix_result.insert(tk.END, f"M = {m}\n\n")
            self.view.matrix_result.insert(tk.END, f"Χωρητικότητα: C = {capacity:.4f} bits/symbol\n\n")

        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα υπολογισμού: {str(e)}")

    def handle_create_chain_matrices(self):
        try:
            num_matrices = int(self.view.num_matrices_entry.get())

            if num_matrices <= 0:
                messagebox.showerror("Σφάλμα", "Θετικός αριθμός μόνο!")
                return

            for widget in self.view.chain_matrices_frame.winfo_children():
                widget.destroy()

            self.view.chain_matrix_widgets = []

            for idx in range(num_matrices):
                matrix_frame = tk.LabelFrame(self.view.chain_matrices_frame,text=f"Πίνακας {idx + 1}",bg=ModernDarkTheme.BG_FRAME,fg=ModernDarkTheme.BG_BLUISH,
                                             font=("Consolas", 10, "bold"))
                matrix_frame.grid(row=idx, column=0, padx=10, pady=8, sticky="ew")

                dims_frame = tk.Frame(matrix_frame, bg=ModernDarkTheme.BG_FRAME)
                dims_frame.pack(pady=4)

                tk.Label(dims_frame, text="Γραμμές:",bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                         font=("Consolas", 11)).grid(row=0, column=0, padx=2)

                rows_entry = tk.Entry(dims_frame, width=5, bg=ModernDarkTheme.BG_ENTRY,
                                      fg=ModernDarkTheme.WHITE_TEXT, font=("Consolas", 11))
                rows_entry.insert(0, "2")
                rows_entry.grid(row=0, column=1, padx=2)

                tk.Label(dims_frame, text="Στήλες:",bg=ModernDarkTheme.BG_FRAME, fg=ModernDarkTheme.WHITE_TEXT,
                         font=("Consolas", 11)).grid(row=0, column=2, padx=2)

                cols_entry = tk.Entry(dims_frame, width=5, bg=ModernDarkTheme.BG_ENTRY, fg=ModernDarkTheme.WHITE_TEXT,
                                      font=("Consolas", 11))
                cols_entry.insert(0, "2")
                cols_entry.grid(row=0, column=3, padx=2)

                create_btn = tk.Button(dims_frame, text="Δημιουργία",bg=ModernDarkTheme.BG_BLUISH, fg="#FFFFFF",font=("Consolas", 9),
                                       command=lambda mf=matrix_frame, re=rows_entry,ce=cols_entry: self.create_single_chain_matrix(mf, re, ce))
                create_btn.grid(row=0, column=4, padx=4)

                entries_frame = tk.Frame(matrix_frame, bg=ModernDarkTheme.BG_FRAME)
                entries_frame.pack(pady=4)

                self.view.chain_matrix_widgets.append({
                    'frame': matrix_frame,
                    'entries_frame': entries_frame,
                    'entries': []
                })

            self.view.chain_result.delete("1.0", tk.END)
            self.view.chain_result.insert(tk.END, f"Δημιουργήθηκαν {num_matrices} πλαίσια πινάκων!\n\nΟρίστε διαστάσεις και πατήστε 'Δημιουργία'\nγια κάθε πίνακα.\n ")

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρο ακέραιο!")

    def create_single_chain_matrix(self, parent_frame, rows_entry, cols_entry):
        try:
            rows = int(rows_entry.get())
            cols = int(cols_entry.get())

            if rows <= 0 or cols <= 0:
                messagebox.showerror("Σφάλμα", "Θετικοί αριθμοί μόνο!")
                return

            matrix_widget = None
            for mw in self.view.chain_matrix_widgets:
                if mw['frame'] == parent_frame:
                    matrix_widget = mw
                    break

            if not matrix_widget:
                return

            for widget in matrix_widget['entries_frame'].winfo_children():
                widget.destroy()

            matrix_widget['entries'] = []

            for i in range(rows):
                row_entries = []
                for j in range(cols):
                    entry = tk.Entry(matrix_widget['entries_frame'], width=8,bg="#393E46", fg=ModernDarkTheme.WHITE_TEXT,font=("Consolas", 11),
                                     justify='center',insertbackground=ModernDarkTheme.WHITE_TEXT)
                    entry.insert(0, f"{1.0 / cols:.2f}")
                    entry.grid(row=i, column=j, padx=1, pady=1)
                    row_entries.append(entry)
                matrix_widget['entries'].append(row_entries)

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρους ακέραιους!")

    def handle_calculate_chain(self):
        try:
            matrices = []
            for idx, mw in enumerate(self.view.chain_matrix_widgets):
                if not mw['entries']:
                    raise ValueError(f"Ο Πίνακας {idx + 1} δεν έχει δημιουργηθεί!")

                matrix_data = []
                for row in mw['entries']:
                    row_values = [float(entry.get()) for entry in row]

                    # Validate
                    if not self.model.check_for_correct_probabilities(row_values):
                        raise ValueError(f"Για τον Πίνακα {idx + 1}: Οι τιμές θα πρέπει να είναι απο 0 έως 1!")

                    matrix_data.append(row_values)

                matrices.append(np.array(matrix_data))

            if not matrices:
                raise ValueError("Δημιουργήστε τουλάχιστον έναν πίνακα!")

            is_valid, error_msg = self.model.check_for_matrix_dimensions(matrices)
            if not is_valid:
                raise ValueError(f"Μη συμβατές διαστάσεις: {error_msg}")

            P_combined = self.model.combine_matrices(matrices)

            m = int(self.view.m_chain_entry.get())
            if m <= 0:
                raise ValueError("Το M πρέπει να είναι θετικός ακέραιος!")

            capacity, x_optimal = self.model.calculate_uniform_channel_capacity(m, P_combined, 1)

            self.view.chain_result.delete("1.0", tk.END)
            self.view.chain_result.insert(tk.END, "--- Αποτελέσματα ---\n")
            self.view.chain_result.insert(tk.END, "\nΑΛΥΣΙΔΑ ΚΑΝΑΛΙΩΝ\n")

            for idx, matrix in enumerate(matrices):

                self.view.chain_result.insert(tk.END, f"Πίνακας P{idx + 1}:\n")
                self.view.chain_result.insert(tk.END, f"{matrix}\n\n")

            self.view.chain_result.insert(tk.END, "Τελικός Πίνακας (P₁ × P₂ × ... × Pₙ):\n")
            self.view.chain_result.insert(tk.END, f"{P_combined}\n\n")

            self.view.chain_result.insert(tk.END, f"M = {m}\n\n")
            self.view.chain_result.insert(tk.END, f"Χωρητικότητα Αλυσίδας: C = {capacity:.4f} bits/symbol\n\n")


        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα υπολογισμού: {str(e)}")



