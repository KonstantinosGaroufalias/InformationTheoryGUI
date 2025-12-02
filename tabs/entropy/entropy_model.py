"""Model: Entropy calculations and business logic"""
import numpy as np


class EntropyModel:
    """Handles all entropy-related calculations"""
    def calculate_entropy(self, p):
        """H(X) = -Σ p_i log2(p_i)"""
        p = np.array(p)[np.array(p) > 0]
        return -np.sum(p * np.log2(p))

    def calculate_information(self, p):
        """I(x) = -log2(p(x))"""
        return -np.log2(p)

    def calculate_kl_divergence(self, P, Q):
        """D(P||Q) = Σ P_i log2(P_i / Q_i)"""
        P, Q = map(np.array, (P, Q))
        return np.sum(P * np.log2(P / Q))

    def calculate_joint_entropy(self, P_XY):
        """H(X,Y)"""
        P = np.array(P_XY)
        return -np.sum(P * np.log2(P + 1e-12))

    def calculate_conditional_entropy(self, P_XY):
        """H(X|Y)"""
        P_XY = np.array(P_XY)
        P_Y = P_XY.sum(axis=0)
        return -np.sum(P_XY * np.log2(P_XY / P_Y + 1e-12))

    def check_sum(self, p, tolerance=0.01):
        """Validate that probabilities sum to 1"""
        return np.isclose(sum(p), 1.0, atol=tolerance)
