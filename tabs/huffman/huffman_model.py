"""Model: Huffman coding and code analysis logic"""
import numpy as np
from collections import Counter
import heapq


class HuffmanModel:
    """Handles all Huffman coding and code analysis calculations"""
    def calculate_avrg_length(self, code_dict, probabilities):
        """L = Σ p(x)l(x)"""
        return np.sum([len(code) * probabilities[symbol]
                       for symbol, code in code_dict.items()])

    def calculate_entropy_from_dictionary(self, probabilities):
        """Shannon entropy"""
        probs = np.array(list(probabilities.values()))
        probs = probs[probs > 0]
        return -np.sum(probs * np.log2(probs))

    def is_non_singular(self, code_dict):
        """Check if code is non-singular"""
        return len(set(code_dict.values())) == len(code_dict)

    def is_instantaneous(self, code_dict):
        """Check if code is prefix-free"""
        codes = list(code_dict.values())
        for i in range(len(codes)):
            for j in range(len(codes)):
                if i != j and codes[i].startswith(codes[j]):
                    return False
        return True

    def kraft_inequality(self, code_dict):
        """Check Kraft inequality"""
        lengths = np.array([len(code) for code in code_dict.values()])
        kraft_sum = np.sum(2.0 ** (-lengths))
        return kraft_sum, kraft_sum <= 1

    def generate_huffman_codes(self, text):
        """Generate Huffman codes from text"""
        freq = Counter(text)
        total = len(text)

        heap = [[count, [char, ""]] for char, count in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        codes = {char: code for char, code in heap[0][1:]}
        probs = {c: freq[c] / total for c in freq}

        return codes, probs, freq
