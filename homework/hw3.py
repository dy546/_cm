import cmath

def solve_cubic(a, b, c, d):
    if a == 0:
        raise ValueError("Not a cubic equation")

    # Normalize
    b /= a; c /= a; d /= a

    # Depressed cubic: t^3 + pt + q = 0
    p = c - b**2/3
    q = 2*b**3/27 - b*c/3 + d

    # Discriminant
    Δ = (q/2)**2 + (p/3)**3

    # Cube roots
    u = (-q/2 + cmath.sqrt(Δ))**(1/3)
    v = (-q/2 - cmath.sqrt(Δ))**(1/3)

    t1 = u + v
    t2 = -(u+v)/2 + (u-v)*cmath.sqrt(3)/2j
    t3 = -(u+v)/2 - (u-v)*cmath.sqrt(3)/2j

    # Back-substitute x = t - b/3
    return [t1 - b/3, t2 - b/3, t3 - b/3]

if __name__ == "__main__":
    print(solve_cubic(1, -6, 11, -6))
    print(solve_cubic(1, -9, 26, -24))