import tkinter as tk
from tkinter import messagebox
import numpy as np


class EntropyController:
    """Το Controller λειτουργεί ως μεσολαβητής μεταξύ του Model και του View"""

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._bind_commands()

    def _bind_commands(self):
        """Σύνδεση όλων των button σε μεθόδους"""
        self.view.calc_entropy_btn.config(command=self.handle_calc_entropy)
        self.view.calc_kl_btn.config(command=self.handle_calc_kl)
        self.view.calc_joint_btn.config(command=self.handle_calc_joint_entropy)
        self.view.calc_mi_btn.config(command=self.handle_calc_mutual_info)
        self.view.calc_cond_btn.config(command=self.handle_calc_conditional)


    def handle_calc_entropy(self):
        try:
            p = [float(x) for x in self.view.prob_entry.get().split()]

            if not self.model.check_sum(p):
                messagebox.showerror("Σφάλμα", "Οι πιθανότητες δεν αθροίζουν σε 1.")
                return

            H = self.model.calculate_entropy(p)

            self.view.result_text.delete("1.0", tk.END)
            self.view.result_text.insert(tk.END, "--- Αποτελέσματα ---\n")
            self.view.result_text.insert(tk.END, f"H(X) = {H:.4f} bits/symbol\n\n")

            for i, val in enumerate(p, 1):
                I = self.model.calculate_information(val)
                self.view.result_text.insert(tk.END,f"P{i}={val:.3f} → I={I:.4f} bits\n")

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρες πιθανότητες!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_calc_kl(self):
        try:
            P = [float(x) for x in self.view.P_entry.get().split()]
            Q = [float(x) for x in self.view.Q_entry.get().split()]
            #split() για διαχωρισμό σε λίστα strings με βάση τα κενά διαστήματα όπως
            #τα εισάγει ο χρήστης στη μορφή   0.5 0.4 0.1
            if len(P) != len(Q):
                raise ValueError("Οι κατανομές πρέπει να έχουν ίδιο μήκος.")

            if not (self.model.check_sum(P) and
                    self.model.check_sum(Q)):
                raise ValueError("Οι κατανομές πρέπει να αθροίζουν σε 1.")

            d_pq = self.model.calculate_kl_divergence(P, Q)
            d_qp = self.model.calculate_kl_divergence(Q, P)

            self.view.kl_result_text.delete("1.0", tk.END)
            self.view.kl_result_text.insert(tk.END, "--- Αποτελέσματα ---\n")
            self.view.kl_result_text.insert(tk.END, f"P = {P}\n")
            self.view.kl_result_text.insert(tk.END, f"Q = {Q}\n\n")
            self.view.kl_result_text.insert(tk.END, f"D(P‖Q) = {d_pq:.6f} bits\n")
            self.view.kl_result_text.insert(tk.END, f"D(Q‖P) = {d_qp:.6f} bits\n")

        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_calc_joint_entropy(self):
        try:
            px = [float(x) for x in self.view.px_entry.get().split()]
            py = [float(x) for x in self.view.py_entry.get().split()]

            if not self.model.check_sum(px):
                messagebox.showerror("Σφάλμα", "Το Px δεν αθροίζει σε 1!")
                return
            if not self.model.check_sum(py):
                messagebox.showerror("Σφάλμα", "Το Py δεν αθροίζει σε 1!")
                return

            px_array = np.array(px)
            py_array = np.array(py)
            P_XY = np.vstack([px_array, py_array])

            H_XY = self.model.calculate_joint_entropy(P_XY)

            self.view.joint_result_text.delete("1.0", tk.END)
            self.view.joint_result_text.insert(tk.END, "ΣΥΝΔΕΤΙΚΗ ΕΝΤΡΟΠΙΑ\n")
            self.view.joint_result_text.insert(tk.END, f"Px = {px}\n")
            self.view.joint_result_text.insert(tk.END, f"Py = {py}\n\n")
            self.view.joint_result_text.insert(tk.END, "Πίνακας P(X,Y):\n")
            self.view.joint_result_text.insert(tk.END, f"{P_XY}\n\n")
            self.view.joint_result_text.insert(tk.END, f"H(X,Y) = {H_XY:.4f} bits\n")

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρες πιθανότητες!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_calc_mutual_info(self):
        try:
            px = [float(x) for x in self.view.mi_px_entry.get().split()]
            py = [float(x) for x in self.view.mi_py_entry.get().split()]

            if not self.model.check_sum(px):
                messagebox.showerror("Σφάλμα", "Το Px δεν αθροίζει σε 1!")
                return
            if not self.model.check_sum(py):
                messagebox.showerror("Σφάλμα", "Το Py δεν αθροίζει σε 1!")
                return


            px_array = np.array(px)
            py_array = np.array(py)
            P_XY = np.vstack([px_array, py_array])

            Hx = self.model.calculate_entropy(px)
            Hy = self.model.calculate_entropy(py)
            Hxy = self.model.calculate_joint_entropy(P_XY)

            Ixy = Hx + Hy - Hxy  # I(X;Y) = H(X) + H(Y) - H(X,Y)

            self.view.mi_result_text.delete("1.0", tk.END)
            self.view.mi_result_text.insert(tk.END, "ΔΙΑΠΛΗΡΟΦΟΡΙΑ I(X;Y)\n")

            self.view.mi_result_text.insert(tk.END, f"Px = {px}\n")
            self.view.mi_result_text.insert(tk.END, f"Py = {py}\n\n")
            self.view.mi_result_text.insert(
                tk.END, f"I(X;Y) = H(X)+H(Y) -H(X,Y) = {Ixy:.14f} bits/symbol\n"
            )

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρες πιθανότητες!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def handle_calc_conditional(self):
        try:
            px = [float(x) for x in self.view.cond_px_entry.get().split()]
            py = [float(x) for x in self.view.cond_py_entry.get().split()]

            if not self.model.check_sum(px):
                messagebox.showerror("Σφάλμα", "Το Px δεν αθροίζει σε 1!")
                return
            if not self.model.check_sum(py):
                messagebox.showerror("Σφάλμα", "Το Py δεν αθροίζει σε 1!")
                return

            px_array = np.array(px)
            py_array = np.array(py)
            P_XY = np.vstack([px_array, py_array])

            Hx = self.model.calculate_entropy(px)
            Hy = self.model.calculate_entropy(py)
            Hxy = self.model.calculate_joint_entropy(P_XY)

            # H(Y|X) = H(X,Y) - H(X)
            # H(X|Y) = H(X,Y) - H(Y)
            Hy_given_x = Hxy - Hx
            Hx_given_y = Hxy - Hy

            self.view.cond_result_text.delete("1.0", tk.END)
            self.view.cond_result_text.insert(tk.END, "ΥΠΟ-ΣΥΝΘΗΚΗ ΕΝΤΡΟΠΙΑ\n")

            self.view.cond_result_text.insert(tk.END, f"Px = {px}\n")
            self.view.cond_result_text.insert(tk.END, f"Py = {py}\n\n")
            self.view.cond_result_text.insert(
                tk.END, f"H(Y|X) = H(X,Y) - H(X) = {Hy_given_x:.4f} bits\n"
            )
            self.view.cond_result_text.insert(
                tk.END, f"H(X|Y) = H(X,Y) - H(Y) = {Hx_given_y:.4f} bits\n"
            )

        except ValueError:
            messagebox.showerror("Σφάλμα", "Παρακαλώ εισάγετε έγκυρες πιθανότητες!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
