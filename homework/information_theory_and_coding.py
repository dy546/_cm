import math
import random

def separator(title):
    print(f"\n{'='*20} {title} {'='*20}")

# ==========================================
# Task 1 & 2: Probability & Log Probability
# ==========================================
separator("1. & 2. Probability of 10,000 Heads")

p = 0.5
n = 10000

# Task 1: Direct Calculation
# This will result in 0.0 due to floating point underflow
prob_direct = p ** n
print(f"Direct Calculation (0.5^10000): {prob_direct}")
print("(Note: The result is 0.0 because the number is too small for standard float precision.)")

# Task 2: Log Calculation
# Using log2 for bits
log_prob = n * math.log2(p)
print(f"Log Probability (n * log2(p)):  {log_prob:.4f} bits")
print(f"Meaning: This event has a self-information of {-log_prob:.4f} bits.")

# ==========================================
# Task 3: Entropy, CE, KL, MI
# ==========================================
separator("3. Information Theory Metrics")

def entropy(P):
    """H(P) = - sum(p * log2(p))"""
    return -sum(p * math.log2(p) for p in P if p > 0)

def cross_entropy(P, Q):
    """H(P, Q) = - sum(p * log2(q))"""
    return -sum(p * math.log2(q) for p, q in zip(P, Q) if q > 0)

def kl_divergence(P, Q):
    """D_KL(P || Q) = sum(p * log2(p/q))"""
    # Note: D_KL(P||Q) = H(P,Q) - H(P)
    return sum(p * math.log2(p / q) for p, q in zip(P, Q) if p > 0 and q > 0)

def mutual_information(P_X, P_Y, P_XY):
    """I(X;Y) = sum(sum(p(x,y) * log2(p(x,y) / (p(x)*p(y)))))"""
    mi = 0
    for i, px in enumerate(P_X):
        for j, py in enumerate(P_Y):
            pxy = P_XY[i][j]
            if pxy > 0:
                mi += pxy * math.log2(pxy / (px * py))
    return mi

# Example Distributions
P = [0.5, 0.5]       # Fair coin
Q = [0.8, 0.2]       # Biased coin (Model)

print(f"Distribution P: {P}")
print(f"Distribution Q: {Q}")
print(f"Entropy H(P):           {entropy(P):.4f} bits")
print(f"Cross Entropy H(P, Q):  {cross_entropy(P, Q):.4f} bits")
print(f"KL Divergence D_KL(P||Q): {kl_divergence(P, Q):.4f} bits")

# Mutual Information Example
# X: Rain (No, Yes), Y: Cloudy (No, Yes)
# P(X) = [0.8, 0.2], P(Y) = [0.7, 0.3]
# Joint P(X,Y) matrix
P_XY = [[0.65, 0.15], # X=No
        [0.05, 0.15]] # X=Yes
P_X = [0.8, 0.2]
P_Y = [0.7, 0.3]

print(f"Mutual Info I(X;Y):       {mutual_information(P_X, P_Y, P_XY):.4f} bits")

# ==========================================
# Task 4: Verify Cross Entropy Inequality
# ==========================================
separator("4. Verification of H(p,p) vs H(p,q)")

# The prompt asked to verify cross_entropy(p,p) > cross_entropy(p,q).
# However, Gibbs' Inequality states H(P,Q) >= H(P).
# So H(P, P) (which is Entropy) is usually LESS than H(P, Q).

ce_pp = cross_entropy(P, P)
ce_pq = cross_entropy(P, Q)

print(f"H(P, P) [Entropy]:      {ce_pp:.4f}")
print(f"H(P, Q) [Cross Ent]:    {ce_pq:.4f}")
print(f"Check: H(P, P) > H(P, Q)? {ce_pp > ce_pq}")
print("Conclusion: The hypothesis provided in the prompt is False.")
print("Fact: Cross Entropy is minimized when Q = P.")


# ==========================================
# Task 5: Hamming (7,4) Code
# ==========================================
separator("5. Hamming (7,4) Encode & Decode")

class Hamming74:
    def __init__(self):
        # Generator Matrix G
        # Maps 4 data bits to 7 codewords
        self.G = [
            [1, 1, 0, 1], # p1
            [1, 0, 1, 1], # p2
            [1, 0, 0, 0], # d1
            [0, 1, 1, 1], # p3
            [0, 1, 0, 0], # d2
            [0, 0, 1, 0], # d3
            [0, 0, 0, 1]  # d4
        ]
        
        # Parity Check Matrix H
        # Used to calculate syndrome
        self.H = [
            [1, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [0, 0, 0, 1, 1, 1, 1]
        ]

    def encode(self, data):
        """Expects a list of 4 bits, e.g., [1, 0, 1, 1]"""
        if len(data) != 4:
            raise ValueError("Data must be 4 bits")
        
        # d1, d2, d3, d4 = data
        # p1 = d1 + d2 + d4
        # p2 = d1 + d3 + d4
        # p3 = d2 + d3 + d4
        
        d1, d2, d3, d4 = data
        p1 = (d1 + d2 + d4) % 2
        p2 = (d1 + d3 + d4) % 2
        p3 = (d2 + d3 + d4) % 2
        
        # Standard Hamming sequence (p1, p2, d1, p3, d2, d3, d4)
        return [p1, p2, d1, p3, d2, d3, d4]

    def decode(self, received):
        """Expects a list of 7 bits"""
        # Calculate Syndrome
        # s1 = p1 + d1 + d2 + d4
        # s2 = p2 + d1 + d3 + d4
        # s3 = p3 + d2 + d3 + d4
        
        r = received # alias
        # Bit positions (0-indexed): 0  1  2   3  4   5   6
        # Correspond to:             p1 p2 d1 p3 d2 d3 d4
        
        s1 = (r[0] + r[2] + r[4] + r[6]) % 2
        s2 = (r[1] + r[2] + r[5] + r[6]) % 2
        s3 = (r[3] + r[4] + r[5] + r[6]) % 2
        
        syndrome_idx = s1 * 1 + s2 * 2 + s3 * 4
        
        corrected = list(r)
        error_status = "No Error"
        
        if syndrome_idx != 0:
            error_status = f"Error at position {syndrome_idx} (1-based)"
            # Flip the bit at index (syndrome_idx - 1)
            corrected[syndrome_idx - 1] = 1 - corrected[syndrome_idx - 1]
            
        # Extract data bits (indices 2, 4, 5, 6)
        decoded_data = [corrected[2], corrected[4], corrected[5], corrected[6]]
        return decoded_data, error_status, corrected

# Test Hamming
hamming = Hamming74()
original_data = [1, 0, 1, 1]
encoded = hamming.encode(original_data)
print(f"Original Data: {original_data}")
print(f"Encoded (7 bits): {encoded}")

# Simulate an error (flip bit at index 4, which is the 5th bit)
received_with_error = list(encoded)
received_with_error[4] = 1 - received_with_error[4]
print(f"Received (Error): {received_with_error}")

decoded_data, status, corrected_code = hamming.decode(received_with_error)
print(f"Decode Status: {status}")
print(f"Corrected Code: {corrected_code}")
print(f"Decoded Data: {decoded_data}")