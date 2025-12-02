"""Model: Channel capacity calculations and business logic"""
import numpy as np
import cvxpy as cp
from scipy.special import xlogy


class ChannelModel:
    """Handles all channel-related calculations"""

    # ───── BSC (Binary Symmetric Channel) ─────────────────────────────

    def calculate_bsc_capacity(self, e):
        """
        Calculate Binary Symmetric Channel capacity
        C_BSC(e) = 1 - H(e) where H(e) is the binary entropy function

        Args:
            e: Error probability [0, 1]

        Returns:
            Capacity in bits/symbol
        """
        if e in (0, 1):
            return 0
        return 1 + e * np.log2(e) + (1 - e) * np.log2(1 - e)

    def generate_bsc_curve_graphics(self, num_points=200):
        """
        Generate BSC capacity curve data for plotting

        Args:
            num_points: Number of points to generate

        Returns:
            x_values, y_values: Arrays for plotting
        """
        x = np.linspace(0.001, 0.99, num_points)
        y = [self.calculate_bsc_capacity(e) for e in x]
        return x, y

    # ───── Channel Matrix Capacity ────────────────────────────────────

    def calculate_uniform_channel_capacity(self, m, P, sum_x=1):
        """
        Calculate channel capacity using convex optimization

        Args:
            m: Number of input symbols
            P: Channel transition matrix P(Y|X) of shape (m, n)
            sum_x: Constraint sum (default=1)

        Returns:
            capacity: Channel capacity in bits/symbol
            x_optimal: Optimal input distribution
        """
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

    # ───── Matrix Validation ──────────────────────────────────────────

    def check_for_correct_probabilities(self, values):
        """
        Validate that all values are in [0, 1]

        Args:
            values: List or array of probability values

        Returns:
            Boolean
        """
        return all(0 <= v <= 1 for v in values)

    # ───── Cascaded Channels ──────────────────────────────────────────

    def combine_matrices(self, matrices):
        """
        Combine multiple channel matrices (cascade/chain)
        P_combined = P₁ × P₂ × P₃ × ... × Pₙ

        Args:
            matrices: List of numpy arrays representing channel matrices

        Returns:
            combined_matrix: Product of all matrices
        """
        if not matrices:
            raise ValueError("No matrices provided!")

        combined_matrix = matrices[0]
        for matrix in matrices[1:]:
            combined_matrix = combined_matrix @ matrix
        return combined_matrix

    def check_for_matrix_dimensions(self, matrices):
        """
        Validate that matrices can be multiplied (compatible dimensions)

        Args:
            matrices: List of numpy arrays

        Returns:
            is_valid: Boolean
            error_msg: Error message if invalid
        """
        for i in range(len(matrices) - 1):
            if matrices[i].shape[1] != matrices[i + 1].shape[0]:
                return False, f"Matrix {i + 1} columns ({matrices[i].shape[1]}) != Matrix {i + 2} rows ({matrices[i + 1].shape[0]})"
        return True, ""
