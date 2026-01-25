import numpy as np

class EntropyModel:
    """Περιέχει όλες της συναρτήσεις του Entropy tab για τους απαραίτητους υπολογισμούς"""
    def calculate_entropy(self, p):
        p = np.array(p)[np.array(p) > 0]
        return -np.sum(p * np.log2(p))

    def calculate_information(self, p):
        return -np.log2(p)

    def calculate_kl_divergence(self, P, Q):
        P, Q = map(np.array, (P, Q))
        return np.sum(P * np.log2(P / Q))

    def calculate_joint_entropy(self, P_XY):
        P = np.array(P_XY)
        return -np.sum(P * np.log2(P))

    def calculate_conditional_entropy(self, P_XY):
        P_XY = np.array(P_XY)
        P_Y = P_XY.sum(axis=0)
        return -np.sum(P_XY * np.log2(P_XY / P_Y))

    def check_sum(self, p):
        """Ελέγχει αν το άθροισμα των πιθανοτήτων είναι 1.0"""
        return np.isclose(sum(p), 1.0)
