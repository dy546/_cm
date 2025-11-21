## Homework 8

# Code Explanation: Information Theory & Hamming Codes

This document provides a detailed breakdown of the Python script `information_theory_and_coding.py`. It explains the mathematical concepts behind the functions and how the Python code implements them.

---

## 1. Probability Underflow & Logarithms

### The Problem
We want to calculate the probability of a fair coin landing on heads 10,000 times in a row.
Mathematical formula: $P = 0.5^{10000}$.

### The Code Logic
```python
# Task 1: Direct Calculation
prob_direct = p ** n  # Results in 0.0
```
* Why it fails: Computers store numbers using "floating point" precision (IEEE 754). The number $0.5^{10000}$ is approximately $1 \times 10^{-3010}$. Most standard float types cannot store numbers smaller than $1 \times 10^{-308}$ (approx). The computer treats it as 0.0 (Underflow).

## The Solution (Log Probability)
```Python
# Task 2: Log Calculation
log_prob = n * math.log2(p)
```

* The Math: We use the logarithm power rule: $\log(p^n) = n \cdot \log(p)$.
* Why it works: instead of multiplying tiny probabilities (which get smaller and smaller), we add their logarithms.$\log_2(0.5) = -1$.$10000 \times -1 = -10000$.
* Interpretation: The result -10000 bits means the event is extremely rare. In machine learning, we almost always use Log Probability (or Log Likelihood) to prevent underflow.

---
## 2. Information Theory Metrics


These functions quantify uncertainty and information distance between probability distributions.
## A. Entropy ($H(P)$)
```Python
def entropy(P):
    return -sum(p * math.log2(p) for p in P if p > 0)
```
* Concept: The average uncertainty in a random variable.
* Code Detail: We iterate through the list of probabilities P. We include if p > 0 because $\log(0)$ is undefined.
## B. Cross Entropy ($H(P, Q)$)
```Python
def cross_entropy(P, Q):
    return -sum(p * math.log2(q) for p, q in zip(P, Q) if q > 0)
```
* Concept: The average number of bits needed to identify an event from distribution $P$, if we use a coding scheme optimized for distribution $Q$.
* Code Detail: zip(P, Q) pairs elements from both lists (e.g., (p[0], q[0]), (p[1], q[1])).
## C. KL Divergence ($D_{KL}(P || Q)$)
```Python
def kl_divergence(P, Q):
    return sum(p * math.log2(p / q) for p, q in zip(P, Q) if ...)
```
* Concept: The "distance" between two distributions. It represents the extra bits required if we use Q to model P.
* Relationship: $D_{KL}(P || Q) = H(P, Q) - H(P)$.
## D. Mutual Information ($I(X; Y)$)
```Python
def mutual_information(P_X, P_Y, P_XY):
    # ... nested loops ...
    mi += pxy * math.log2(pxy / (px * py))
```
* Concept: Measures how much knowing variable X reduces uncertainty about variable Y.
* Code Detail: We loop through every combination of X and Y.
    * If X and Y are independent, $P(x,y) = P(x)P(y)$, so the log term becomes $\log(1) = 0$, and Mutual Info is 0.
---

## 3. Inequality Verification

The script checks the relationship between Self-Entropy and Cross-Entropy.
```Python
ce_pp = cross_entropy(P, P)  # This is just Entropy
ce_pq = cross_entropy(P, Q)  # Cross Entropy
print(f"Check: H(P, P) > H(P, Q)? {ce_pp > ce_pq}")
```
* The Result: False.
* Explanation: By Gibbs' Inequality, $H(P, Q) \ge H(P)$.
    * Cross Entropy is minimized when the predicted distribution $Q$ is exactly the same as the true distribution $P$.
    * Therefore, $H(P, P)$ is smaller (better) than $H(P, Q)$ when $P \neq Q$.
---
## 4. Hamming (7,4) Code
This section implements error-correcting code. It takes 4 bits of data and adds 3 parity bits to make a 7-bit "codeword".
### A. The Setup
* Data: 4 bits ($d_1, d_2, d_3, d_4$).
* Parity: 3 bits ($p_1, p_2, p_3$).
* Total: 7 bits.
### B. Encoding
```Python
p1 = (d1 + d2 + d4) % 2
p2 = (d1 + d3 + d4) % 2
p3 = (d2 + d3 + d4) % 2
```
* Logic: Each parity bit covers a specific subset of data bits.
    * If the sum of bits in the set is even, parity is 0. If odd, parity is 1.
    * % 2 (modulo) performs this "XOR" summation.
### C. Decoding & Syndrome Calculation
When the receiver gets the 7 bits, they might contain noise (flipped bits).
```Python
s1 = (r[0] + r[2] + r[4] + r[6]) % 2
s2 = (r[1] + r[2] + r[5] + r[6]) % 2
s3 = (r[3] + r[4] + r[5] + r[6]) % 2
```
* The Syndrome: We recalculate the parity checks on the received bits.
    * If s1, s2, s3 are all 0, there is no error.
    * If they are not 0, the binary number s3 s2 s1 tells us exactly which position (index) has the error.
### D. Error Correction
```Python
syndrome_idx = s1 * 1 + s2 * 2 + s3 * 4
if syndrome_idx != 0:
    # Flip the bit back
    corrected[syndrome_idx - 1] = 1 - corrected[syndrome_idx - 1]
```
* Logic:
    * We convert the binary syndrome to an integer index.
    * 1 - x is a mathematical trick to flip a bit:
        * $1 - 1 = 0$
        * $1 - 0 = 1$
    * This allows the code to self-repair single-bit errors.