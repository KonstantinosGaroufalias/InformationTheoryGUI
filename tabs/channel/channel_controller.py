from tkinter import messagebox
import numpy as np


class ChannelController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._bind_commands()

    def _bind_commands(self):
        self.view.calc_bsc_btn.config(command=self.handle_calc_bsc)
        self.view.create_matrix_btn.config(command=self.handle_create_matrix)
        self.view.calc_capacity_btn.config(command=self.handle_calculate_capacity)
        self.view.create_chain_btn.config(command=self.handle_create_chain_matrices)
        self.view.calc_chain_btn.config(command=self.handle_calculate_chain)

    def handle_calc_bsc(self):
        try:
            e = float(self.view.e_entry.get())
            if not 0 <= e <= 1:
                raise ValueError("Το e(bit error rate) πρέπει να ανήκει στο διάστημα 0 έως 1")

            C = self.model.calculate_bsc_capacity(e)
            x_vals, y_vals = self.model.generate_bsc_curve_graphics()

            self.view.display_bsc_result(e, C)
            self.view.update_bsc_plot(x_vals, y_vals, e, C)

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

            self.view.create_matrix_grid(rows, cols)
            self.view.display_matrix_creation_success(rows, cols)

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρους ακέραιους αριθμούς!")

    def handle_calculate_capacity(self):
        try:
            if not self.view.matrix_entries:
                messagebox.showerror("Σφάλμα", "Μη βιάζεστε! Δημιουργήστε πρώτα έναν πίνακα!")
                return

            # Extract matrix data (reusable function)
            matrix_data = self._extract_matrix_data(self.view.matrix_entries, "Πίνακας")
            P_YX = np.array(matrix_data)

            m = int(self.view.m_entry.get())
            if m <= 0:
                raise ValueError("Το M πρέπει να είναι θετικός ακέραιος!")

            capacity, x_optimal = self.model.calculate_uniform_channel_capacity(m, P_YX, 1)
            self.view.display_capacity_result(P_YX, m, capacity)

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

            self.view.create_chain_matrices(num_matrices)
            self.view.display_chain_frames_created(num_matrices)

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρο ακέραιο!")

    def handle_calculate_chain(self):
        """Extract and validate all chain matrices - reuses same logic as 2nd subtab!"""
        try:
            matrices = []

            # For each chain matrix, extract data (same way as 2nd subtab)
            for idx, frame_data in enumerate(self.view.chain_frames):
                if not frame_data['matrix_entries']:
                    raise ValueError(f"Ο Πίνακας {idx + 1} δεν έχει δημιουργηθεί!")

                # Reuse the same extraction logic!
                matrix_data = self._extract_matrix_data(frame_data['matrix_entries'], f"Πίνακας {idx + 1}")
                matrices.append(np.array(matrix_data))

            if not matrices:
                raise ValueError("Δημιουργήστε τουλάχιστον έναν πίνακα!")

            # Check dimension compatibility for matrix multiplication
            is_valid, error_msg = self.model.check_for_matrix_dimensions(matrices)
            if not is_valid:
                raise ValueError(f"Μη συμβατές διαστάσεις: {error_msg}")

            # Combine matrices
            P_combined = self.model.combine_matrices(matrices)

            m = int(self.view.m_chain_entry.get())
            if m <= 0:
                raise ValueError("Το M πρέπει να είναι θετικός ακέραιος!")

            capacity, x_optimal = self.model.calculate_uniform_channel_capacity(m, P_combined, 1)
            self.view.display_chain_result(matrices, P_combined, m, capacity)

        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα υπολογισμού: {str(e)}")

    def _extract_matrix_data(self, matrix_entries, matrix_name):
        """
        Reusable method to extract and validate matrix data from Entry widgets.
        Works for both 2nd subtab (single matrix) and 3rd subtab (multiple matrices).
        """
        matrix_data = []

        for i, row in enumerate(matrix_entries):
            row_values = [float(entry.get()) for entry in row]

            # Validate probabilities
            if not self.model.check_for_correct_probabilities(row_values):
                raise ValueError(f"{matrix_name} - Γραμμή {i + 1}: Όλες οι τιμές πρέπει να είναι στο [0,1]")

            # Warn if row doesn't sum to 1
            if not np.isclose(sum(row_values), 1.0, atol=0.01):
                messagebox.showwarning("Προειδοποίηση",
                                       f"{matrix_name} - Γραμμή {i + 1} αθροίζει σε {sum(row_values):.3f} (όχι 1.0)")

            matrix_data.append(row_values)

        return matrix_data
