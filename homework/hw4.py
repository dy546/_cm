import numpy as np

def root(c):

    while len(c) > 1 and abs(c[-1]) < 1e-14:
        c.pop()

    n = len(c) - 1
    if n == 0:
        return []
    if n == 1:
        return [-c[0] / c[1]]

    c = [ci / c[-1] for ci in c]

    companion = np.zeros((n, n))
    companion[1:, :-1] = np.eye(n-1)
    companion[:, -1] = -np.array(c[:-1])

    roots = np.linalg.eigvals(companion)
    return roots

if __name__ == "__main__":
    coeffs = [-24, 26, -9, 1]
    print(root(coeffs))
    coeffs = [720, -1764, 1624, -735, 175, -21, 1] 
    print(root(coeffs))