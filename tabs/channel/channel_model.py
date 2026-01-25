import numpy as np
import cvxpy as cp
from scipy.special import xlogy


class ChannelModel:
    """Περιέχει όλες της συναρτήσεις του Channel tab για τους απαραίτητους υπολογισμούς"""

    def calculate_bsc_capacity(self, e):
        if e in (0, 1):
            return 0
        return 1 + e * np.log2(e) + (1 - e) * np.log2(1 - e)

    def generate_bsc_curve_graphics(self, num_points=200):
        x = np.linspace(0.001, 0.99, num_points)
        y = [self.calculate_bsc_capacity(e) for e in x]
        return x, y


    def calculate_uniform_channel_capacity(self, m, P, sum_x=1):
        try:
            n = m
            x = cp.Variable(shape=n)
            y = P @ x
            c = np.sum(np.array((xlogy(P, P) / np.log(2))), axis=0)
            I = c @ x + cp.sum(cp.entr(y) / np.log(2))
            obj = cp.Maximize(I)
            constraints = [cp.sum(x) == sum_x, x >= 0]
            prob = cp.Problem(obj, constraints)
            prob.solve()

            if prob.status == 'optimal':
                return prob.value, x.value
            else:
                return np.nan, np.nan
        except Exception as e:
            raise ValueError(f"Optimization failed: {str(e)}")

    def check_for_correct_probabilities(self, values):
        return all(0 <= v <= 1 for v in values)

    def combine_matrices(self, matrices):
        if not matrices:
            raise ValueError("No matrices provided!")

        combined_matrix = matrices[0]
        for matrix in matrices[1:]:
            combined_matrix = combined_matrix @ matrix
        return combined_matrix

    def check_for_matrix_dimensions(self, matrices):
        for i in range(len(matrices) - 1):
            if matrices[i].shape[1] != matrices[i + 1].shape[0]:
                return False, f"Matrix {i + 1} columns ({matrices[i].shape[1]}) != Matrix {i + 2} rows ({matrices[i + 1].shape[0]})"
        return True, ""
