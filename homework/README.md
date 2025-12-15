# [HOMEWORK 1](https://github.com/dy546/_cm/blob/c67478f6e8bc109a78438de8afc32446945f2bec/homework/hw1.py)

All copied from GEMINI without modification

This document details a Python script that demonstrates three fundamental concepts in calculus using **numerical analysis**. Instead of utilizing symbolic math (finding exact formulas), the script utilizes a tiny step size, $h$, to approximate limits.

## 1\. The "Infinitesimal" ($h$)

In theoretical calculus, derivatives and integrals rely on the limit as changes approach zero ($h \to 0$). In numerical programming, we cannot use a true zero, so we use a very small fixed number to approximate it.

**Code:**

```python
h = 0.00001
```

  * **Concept:** $h$ represents the "tiny step size" or the numerical approximation of the infinitesimal.

-----

## 2\. Numerical Differentiation (`df`)

The function `df(f, x)` approximates the derivative (the instantaneous slope) of a function $f$ at a point $x$.

### Mathematical Concept

It utilizes the standard limit definition of the derivative, known as the **Forward Difference Quotient**:

$$f'(x) \approx \frac{f(x+h) - f(x)}{h}$$

### Code Logic

```python
def df(f, x):
    return (f(x+h)-f(x))/h
```

**How it works:** It takes a small step forward ($x + h$), finds the change in height (rise), and divides it by the step size (run).

-----

## 3\. Numerical Integration (`integral`)

The function `integral(f, a, b)` approximates the area under the curve $f(x)$ from point $a$ to point $b$.

[Image of left Riemann sum approximation]

### Mathematical Concept

It calculates a **Left Riemann Sum**. It sums up the area of rectangles defined by:
$$\text{Area} \approx \sum_{i} f(x_i) \cdot h$$

### Code Logic

```python
def integral(f, a, b):
    x = a
    area = 0
    while x < b:
        area += f(x) * h
        x += h
    return area
```

**How it works:** The code iterates from `a` to `b` in steps of `h`. At every step, it calculates the area of a thin rectangle (height $f(x) \times$ width $h$) and accumulates it into the total `area`.

-----

## 4\. The Fundamental Theorem of Calculus (`theorem1`)

This function empirically proves the **First Fundamental Theorem of Calculus**, which states that differentiation and integration are inverse processes.

### The Theorem

Taking the derivative of an integral function returns the original function:

$$\frac{d}{dx} \left( \int_{0}^{x} f(t) \, dt \right) = f(x)$$

### Code Logic

```python
def theorem1(f, x):
    # 1. Define the integral function up to x (Inner part)
    # 2. Take the derivative of that integral (Outer part)
    r = df(lambda x: integral(f, 0, x), x)

    print('r=', r, 'f(x)=', f(x))
    
    # Check if the result matches the original function height
    assert abs(r - f(x)) < 0.01
```

### Step-by-Step Execution

1.  **Inner part:** `lambda x: integral(f, 0, x)` creates a temporary function representing the accumulated area under the curve up to $x$. Let's call this $A(x)$.
2.  **Outer part:** `df(..., x)` calculates the rate at which that area $A(x)$ is changing.
3.  **Result:** The rate of change of the area should equal the height of the graph $f(x)$ at that point.

-----

## 5\. Execution Example: $f(x) = x^3$

The script tests these concepts using the cubic function $f(x) = x^3$ at the point $x=2$.

### Comparison Table: Math vs. Code

| Concept | Mathematical Exact Value | Code Approximation | Notes |
| :--- | :--- | :--- | :--- |
| **A. Derivative** | $\frac{d}{dx}(x^3) = 3x^2$ <br> At $x=2$, result is **12** | `df(f, 2)` <br> Returns $\approx$ **12.00006** | Very close approximation. |
| **B. Integral** | $\int_0^2 x^3 dx = [\frac{x^4}{4}]_0^2$ <br> Result is **4** | `integral(f, 0, 2)` <br> Returns $\approx$ **3.9999** | Left Riemann sums slightly underestimate increasing functions. |
| **C. Theorem** | $f(2) = 2^3$ <br> Result is **8** | `theorem1` calculation <br> Returns $\approx$ **8.00** | The assertion `abs(r - 8) < 0.01` passes, verifying the theorem holds numerically. |

-----

# [HOMEWORK 2](https://github.com/dy546/_cm/blob/c67478f6e8bc109a78438de8afc32446945f2bec/homework/hw2.py)

# Quadratic Equation Solver in Python

All copied from GEMINI without modification

This script defines a function to calculate the roots (solutions) of a quadratic equation using the standard quadratic formula. It utilizes Python's `cmath` library to handle both real and complex solutions.

## 1. The Math Behind It

The code solves equations of the form:
$$ax^2 + bx + c = 0$$

To find the values of $x$, it uses the **Quadratic Formula**:

$$ x = \frac{-b \pm \sqrt{b^2-4ac}}{2a} $$

Where:
* $a, b, c$ are the coefficients.
* $b^2 - 4ac$ is known as the **Discriminant ($D$)**.

---

## 2. Code Breakdown

### Importing `cmath`
```python
import cmath
````

  * **Why not `math`?** The standard `math` library will throw an error if you try to find the square root of a negative number.
  * **Why `cmath`?** This stands for "Complex Math." It automatically handles negative discriminants by using complex numbers (numbers involving the imaginary unit $i$, or $j$ in Python).

### The Function `root2(a, b, c)`

```python
def root2(a, b, c):
    D = b**2 - 4*a*c
    
    r1 = (-b + cmath.sqrt(D)) / (2*a)
    r2 = (-b - cmath.sqrt(D)) / (2*a)
    
    return r1, r2
```

1.  **Calculate Discriminant (`D`):** It computes $b^2 - 4ac$.
2.  **Calculate Roots (`r1`, `r2`):**
      * `r1` uses the addition ($+$) part of the formula.
      * `r2` uses the subtraction ($-$) part of the formula.
      * Because `cmath.sqrt` is used, the result is always a complex number object, even if the imaginary part is 0.
3.  **Return:** It returns a tuple containing both solutions.

-----

## 3\. Execution Examples

The `if __name__ == "__main__":` block tests three specific cases.

### Case 1: Two Real Distinct Roots

```python
print(root2(1, -5, 6))
```

  * **Equation:** $x^2 - 5x + 6 = 0$
  * **Discriminant:** $25 - 24 = 1$ (Positive)
  * **Math:** Factors to $(x-3)(x-2)$. Roots are $3$ and $2$.
  * **Output:** `((3+0j), (2+0j))`

### Case 2: Two Real Distinct Roots (Negative)

```python
print(root2(1, 4, 3))
```

  * **Equation:** $x^2 + 4x + 3 = 0$
  * **Discriminant:** $16 - 12 = 4$ (Positive)
  * **Math:** Factors to $(x+1)(x+3)$. Roots are $-1$ and $-3$.
  * **Output:** `((-1+0j), (-3+0j))`

### Case 3: Complex Roots

```python
print(root2(1, 1, 1))
```

  * **Equation:** $x^2 + x + 1 = 0$
  * **Discriminant:** $1 - 4 = -3$ (Negative)
  * **Math:** The square root of $-3$ is imaginary ($i\sqrt{3}$).
  * **Output:** `((-0.5+0.866...j), (-0.5-0.866...j))`
      * *Note: Python uses `j` to represent the imaginary unit $\sqrt{-1}$.*

-----

## Summary

| Input `(a,b,c)` | Discriminant | Root Type |
| :--- | :--- | :--- |
| `(1, -5, 6)` | Positive | Real numbers |
| `(1, 4, 3)` | Positive | Real numbers |
| `(1, 1, 1)` | Negative | Complex numbers (with `j`) |

---
# [HOMEWORK 3](https://github.com/dy546/_cm/blob/c67478f6e8bc109a78438de8afc32446945f2bec/homework/hw3.py)

All copied from GEMINI without modification

# Cubic Equation Solver in Python

This script implements **Cardano’s Method** to solve cubic equations of the form:
$$ax^3 + bx^2 + cx + d = 0$$

Unlike the quadratic formula, the cubic formula is significantly more complex and requires transforming the equation into a simpler form first.

## 1. The Mathematical Strategy

The code follows a specific algorithm to find the roots:

1.  **Normalization:** Divide by $a$ to get $x^3 + \dots = 0$.
2.  **Depression:** Transform the equation to remove the $x^2$ term. This creates a "Depressed Cubic": $t^3 + pt + q = 0$.
3.  **Cardano's Formula:** Solve for $t$ using the discriminant method.
4.  **Back-Substitution:** Convert $t$ back to $x$ to find the final roots.

---

## 2. Code Breakdown

### The Setup and Normalization
```python
def solve_cubic(a, b, c, d):
    if a == 0:
        raise ValueError("Not a cubic equation")
    
    # Normalize
    b /= a; c /= a; d /= a


  * **Validation:** If $a=0$, it is a quadratic equation, not a cubic.
  * **Normalization:** We divide all coefficients by $a$ so the leading term becomes $1x^3$. This simplifies later formulas.

### Creating the "Depressed Cubic"

```python
    # Depressed cubic: t^3 + pt + q = 0
    p = c - b**2/3
    q = 2*b**3/27 - b*c/3 + d
```

To solve the cubic, we substitute $x = t - \frac{b}{3}$.
This clever substitution eliminates the square term ($t^2$), leaving us with a simpler equation:
$$t^3 + pt + q = 0$$
The variables `p` and `q` are derived from the original coefficients using standard algebraic expansion.

### Calculating the Discriminant and "u, v"

```python
    # Discriminant
    Δ = (q/2)**2 + (p/3)**3

    # Cube roots
    u = (-q/2 + cmath.sqrt(Δ))**(1/3)
    v = (-q/2 - cmath.sqrt(Δ))**(1/3)
```

  * **Discriminant ($\Delta$):** This determines the nature of the roots (real vs. complex).
  * **Cardano's terms ($u, v$):** The solution relies on finding two numbers $u$ and $v$ such that $t = u + v$. The `cmath` library is essential here because even if the final answers are real numbers (like 1, 2, 3), the intermediate steps often involve the square roots of negative numbers.

### Finding the 3 Roots ($t_1, t_2, t_3$)

```python
    t1 = u + v
    t2 = -(u+v)/2 + (u-v)*cmath.sqrt(3)/2j
    t3 = -(u+v)/2 - (u-v)*cmath.sqrt(3)/2j
```

A cubic equation always has 3 roots.

1.  **$t_1$:** The straightforward sum $u + v$.
2.  **$t_2, t_3$:** These are found using the **complex cube roots of unity** ($\omega$).
    The formula uses $-\frac{1}{2} \pm i\frac{\sqrt{3}}{2}$ to rotate the solutions in the complex plane.

### Back-Substitution

```python
    # Back-substitute x = t - b/3
    return [t1 - b/3, t2 - b/3, t3 - b/3]
```

Finally, we reverse the substitution we made in step 2 to get the actual $x$ values. Note that `b` here is the *normalized* value (original $b$ divided by original $a$).

-----

## 3\. Execution Examples

### Case 1: Roots 1, 2, 3

```python
print(solve_cubic(1, -6, 11, -6))
```

  * **Equation:** $x^3 - 6x^2 + 11x - 6 = 0$
  * **Math:** Factors to $(x-1)(x-2)(x-3)$.
  * **Output:** The code will return values extremely close to `1`, `2`, and `3`.
      * *Note:* Due to floating point arithmetic and `cmath` operations, you might see results like `(3+0j)` or `(1.999999999+0j)`.

### Case 2: Roots 2, 3, 4

```python
print(solve_cubic(1, -9, 26, -24))
```

  * **Equation:** $x^3 - 9x^2 + 26x - 24 = 0$
  * **Math:** Factors to $(x-2)(x-3)(x-4)$.
  * **Output:** Returns approximations of `2`, `3`, and `4`.

-----

## Summary Table

| Step | Formula / Concept | Python Implementation |
| :--- | :--- | :--- |
| **Transform** | Substitution $x = t - \frac{b}{3}$ | `p = ...`, `q = ...` |
| **Solve** | $u, v = \sqrt[3]{- \frac{q}{2} \pm \sqrt{\Delta}}$ | `u = (...)**(1/3)` |
| **Rotate** | Roots of unity (Complex plane rotation) | `cmath.sqrt(3)/2j` |
| **Restore** | $x = t - \frac{b}{3}$ | `t1 - b/3` |

---
# [HOMEWORK 4](https://github.com/dy546/_cm/blob/c67478f6e8bc109a78438de8afc32446945f2bec/homework/hw4.py)

All copied from GEMINI without modification

# General Polynomial Solver (Eigenvalue Method)

This script demonstrates a powerful numerical technique to solve polynomial equations of **any degree** (not just quadratic or cubic). Instead of using a specific algebraic formula, it converts the problem into a Linear Algebra problem using a **Companion Matrix**.

## 1. The Mathematical Concept

To solve a polynomial equation $P(x) = 0$, we can construct a special square matrix called the **Companion Matrix**.

The property that makes this useful is:
**The eigenvalues of the Companion Matrix are exactly the roots of the polynomial.**

For a polynomial normalized so the highest term is $1$ (a monic polynomial):
$$x^n + c_{n-1}x^{n-1} + \dots + c_1x + c_0 = 0$$

The Companion Matrix $C$ looks like this:

$$
C = \begin{pmatrix}
0 & 0 & \dots & 0 & -c_0 \\
1 & 0 & \dots & 0 & -c_1 \\
0 & 1 & \dots & 0 & -c_2 \\
\vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & \dots & 1 & -c_{n-1}
\end{pmatrix}
$$

Notice the diagonal of $1$s just below the main diagonal, and the negated coefficients in the last column.

---

## 2. Code Breakdown

### Input Format
The function expects coefficients in **ascending order** of power:
`c = [constant, x^1, x^2, ..., x^n]`

### Pre-processing
```python
    # Remove high-order terms that are effectively zero
    while len(c) > 1 and abs(c[-1]) < 1e-14:
        c.pop()

    # Base cases
    n = len(c) - 1
    if n == 0: return []               # Constant number (no x)
    if n == 1: return [-c[0] / c[1]]   # Linear equation (ax + b = 0)
````

1.  **Cleanup:** The `while` loop ensures we identify the *true* degree of the polynomial. If the user passes `[1, 2, 0, 0]`, it strips the zeros to treat it as degree 1, not degree 3.
2.  **Base Cases:** It handles simple lines or constants instantly to save computation.

### Normalization

```python
    c = [ci / c[-1] for ci in c]
```

The companion matrix method requires the polynomial to be "monic" (the coefficient of the highest power must be 1). We achieve this by dividing every coefficient by the highest coefficient (`c[-1]`).

### Constructing the Companion Matrix

```python
    companion = np.zeros((n, n))
    
    # Fill the sub-diagonal with 1s
    companion[1:, :-1] = np.eye(n-1)
    
    # Fill the last column with negative coefficients
    companion[:, -1] = -np.array(c[:-1])
```

This uses NumPy slicing to build the matrix structure shown in Section 1.

  * `np.eye(n-1)` creates the identity line.
  * `companion[:, -1]` inserts the coefficients into the final column.

### Solving

```python
    roots = np.linalg.eigvals(companion)
    return roots
```

The function `np.linalg.eigvals` (Eigenvalues) performs the heavy lifting using iterative numerical algorithms (like QR decomposition).

-----

## 3\. Execution Examples

### Example 1: Cubic Equation

```python
coeffs = [-24, 26, -9, 1]
print(root(coeffs))
```

  * **Polynomial:** $1x^3 - 9x^2 + 26x - 24 = 0$ (Note the input is reversed: $-24$ is constant, $1$ is $x^3$).
  * **Math:** This factors into $(x-2)(x-3)(x-4)$.
  * **Output:** The code returns an array containing `2.`, `3.`, and `4.` (order may vary).

### Example 2: Sextic (Degree 6) Equation

```python
coeffs = [720, -1764, 1624, -735, 175, -21, 1] 
print(root(coeffs))
```

  * **Polynomial:** $x^6 - 21x^5 + \dots + 720 = 0$.
  * **Math:** This is the expansion of $(x-1)(x-2)(x-3)(x-4)(x-5)(x-6)$.
  * **Output:** The code will return the numbers 1 through 6.

-----

## Summary

| Feature | Description |
| :--- | :--- |
| **Method** | Companion Matrix + Eigenvalues |
| **Library** | `numpy` (Linear Algebra module) |
| **Input Order** | $[c_0, c_1, c_2 \dots c_n]$ (Ascending powers) |
| **Complexity** | Handles real and complex roots automatically |
| **Degree** | Solves for $N$ roots for degree $N$ |

---
# [HOMEWORK 5](https://github.com/dy546/_cm/blob/c67478f6e8bc109a78438de8afc32446945f2bec/homework/hw5.py)

All copied from GEMINI without modification

# Finite Field Implementation in Python

This script provides a robust, object-oriented implementation of **Finite Fields** (specifically Galois Fields of prime order, $GF(p)$). It builds the mathematical structure from the ground up using Abstract Base Classes to enforce group theory axioms.

## 1. Mathematical Foundation

A Finite Field $GF(p)$ consists of a set of integers $\{0, 1, \dots, p-1\}$ with two operations: addition ($+$) and multiplication ($\cdot$). For this structure to be a valid **Field**, it must satisfy specific properties:

1.  **Additive Group:** The set forms a group under addition (Identity: 0).
2.  **Multiplicative Group:** The set (excluding 0) forms a group under multiplication (Identity: 1).
3.  **Distributivity:** Multiplication distributes over addition: $a \cdot (b + c) = (a \cdot b) + (a \cdot c)$.

---

## 2. Code Architecture

### The Abstract Base Class (`Group`)
```python
class Group(ABC):
    @abstractmethod
    def operation(self, a, b): pass
    
    @abstractmethod
    def inverse(self, a): pass
```
This defines the "contract" for any mathematical group. Any subclass **must** implement methods to calculate the group operation and find inverses. This ensures that whether we are doing addition or multiplication, the structure remains consistent.

### The Element (`FiniteFieldElement`)

This class acts as a container for the data. It holds:

  * `value`: The integer number (e.g., 3).
  * `prime`: The modulus $p$ (e.g., 7).
    It ensures that arithmetic always stays within the field by applying `% prime`.

-----

## 3\. Group Implementations

### Additive Group (`FiniteFieldAddGroup`)

This handles the "plus" logic for the field.

  * **Operation:** $(a + b) \pmod p$
  * **Identity:** $0$
  * **Inverse:** The number added to $x$ to get 0. In modular arithmetic, $-x = p - x$.

### Multiplicative Group (`FiniteFieldMulGroup`)

This handles the "times" logic. Note that **0 is excluded** from this group.

  * **Operation:** $(a \cdot b) \pmod p$
  * **Identity:** $1$
  * **Inverse:** The number multiplied by $x$ to get 1.
      * *Algorithm:* The code uses **Fermat's Little Theorem**, which states that $a^{p-2} \equiv a^{-1} \pmod p$.
      * *Code:* `pow(a.value, self._prime - 2, self._prime)`

-----

## 4\. Operator Overloading (`FiniteFieldNumber`)

While the Group classes handle the logic, they are verbose to use (`group.operation(a,b)`). The `FiniteFieldNumber` class wraps these operations using Python "Magic Methods" to allow natural mathematical syntax.

| Python Operator | Method | Logic Implemented |
| :--- | :--- | :--- |
| `+` | `__add__` | `add_group.operation(a, b)` |
| `-` | `__sub__` | `add_group.operation(a, inverse(b))` |
| `*` | `__mul__` | `mul_group.operation(a, b)` |
| `/` | `__truediv__` | `mul_group.operation(a, inverse(b))` |
| `**` | `__pow__` | Repeated multiplication |

**Example of benefit:**
Instead of:

```python
res = field.mul_group.operation(a, field.add_group.operation(b, c))
```

You can write:

```python
res = a * (b + c)
```

-----

## 5\. Automated Axiom Verification

The code includes a comprehensive testing suite to mathematically prove the implementation is correct. It generates random elements and asserts that the following laws hold true:

1.  **Closure:** Result of an operation stays in the set.
2.  **Associativity:** $(a+b)+c = a+(b+c)$.
3.  **Identity:** $a + 0 = a$ and $a \cdot 1 = a$.
4.  **Inverse:** $a + (-a) = 0$ and $a \cdot a^{-1} = 1$.
5.  **Commutativity:** $a+b = b+a$.
6.  **Distributivity:** $a \cdot (b+c) = a\cdot b + a\cdot c$.

## 6\. Execution Flow

When run (`if __name__ == "__main__":`), the script:

1.  Performs a quick check with $GF(5)$.
2.  Runs `run_comprehensive_tests()` which iterates through primes $[2, 3, 5, 7, 11]$.
3.  For each prime, it validates all group and field axioms.
4.  Demonstrates the syntax sugar (operator overloading) and verifies the results against raw group operations.

### Example Output Logic

If calculating in $GF(7)$:

  * `3 + 5` $\rightarrow 8 \pmod 7 = 1$
  * `3 * 5` $\rightarrow 15 \pmod 7 = 1$
  * `1 / 3` $\rightarrow$ Inverse of 3 is 5 (because $3 \times 5 = 15 \equiv 1 \pmod 7$).

---
# [HOMEWORK 6](https://github.com/dy546/_cm/blob/5963b7e95ce45df62ca20bb7f0d7486980e5fa9b/homework/geometry_toolkit.py)

All copied from GEMINI without modification

# Mathematical Explanations for 2D Geometry Toolkit

This document details the mathematical principles used in the `geometry_toolkit.py` script for defining and manipulating 2D geometric objects.

---

## 1. Core Definitions

### Point
A **point** is the most fundamental object in geometry. It represents a precise location in a 2D Cartesian plane and is defined by an ordered pair of coordinates $(x, y)$.

### Line
A **line** is a one-dimensional object representing an infinite set of points extending in opposite directions. It can be defined in several ways. The script uses two primary forms:

1.  **Two-Point Form**: A unique line can be defined by two distinct points, $P_1(x_1, y_1)$ and $P_2(x_2, y_2)$.
2.  **General Form**: The set of all points $(x, y)$ that satisfy the linear equation:
    $$ ax + by + c = 0 $$
    where $a, b, c$ are real constants, and at least one of $a$ or $b$ is non-zero. The vector $\vec{n} = \langle a, b \rangle$ is a normal vector to the line.

### Circle
A **circle** is the set of all points $(x, y)$ in a plane that are at a fixed distance, the **radius** $r$, from a given point, the **center** $(h, k)$. Its equation is:
$$ (x-h)^2 + (y-k)^2 = r^2 $$



---

## 2. Intersection Mathematics

### Line-Line Intersection
To find the intersection of two lines, we solve their system of linear equations:
$$
\begin{cases}
a_1x + b_1y = -c_1 \\
a_2x + b_2y = -c_2
\end{cases}
$$
The determinant of the coefficient matrix is $D = a_1b_2 - a_2b_1$.

-   If $D \neq 0$, the lines intersect at a single, unique point. The coordinates of this point can be found using Cramer's rule:
    $$ x = \frac{-c_1b_2 - (-c_2b_1)}{a_1b_2 - a_2b_1} = \frac{b_1c_2 - b_2c_1}{D} $$
    $$ y = \frac{a_1(-c_2) - a_2(-c_1)}{a_1b_2 - a_2b_1} = \frac{a_2c_1 - a_1c_2}{D} $$
-   If $D = 0$, the lines are parallel. They have no intersection unless they are also coincident (the same line), in which case they have infinite intersection points.

### Line-Circle Intersection
To find the intersection of a line ($ax + by + c = 0$) and a circle ($(x-h)^2 + (y-k)^2 = r^2$), we substitute one equation into the other.

1.  Isolate a variable from the line equation. For example, if $b \neq 0$, we get:
    $$ y = \frac{-ax - c}{b} $$
2.  Substitute this expression for $y$ into the circle's equation:
    $$ (x-h)^2 + \left(\left(\frac{-ax - c}{b}\right) - k\right)^2 = r^2 $$
3.  Expanding and rearranging this equation yields a quadratic equation of the form $Ax^2 + Bx + C = 0$.
4.  The number of solutions is determined by the **discriminant**, $\Delta = B^2 - 4AC$:
    -   $\Delta > 0$: Two distinct real roots for $x$. This corresponds to **two intersection points**.
    -   $\Delta = 0$: One real root for $x$. The line is **tangent** to the circle at one point.
    -   $\Delta < 0$: No real roots. The line and circle **do not intersect**.

### Circle-Circle Intersection
To find the intersection of two circles, we can simplify the problem by first finding the equation of their **radical axis**.

1.  Start with the equations of two circles:
    $$ C_1: (x-h_1)^2 + (y-k_1)^2 = r_1^2 \implies x^2 - 2h_1x + h_1^2 + y^2 - 2k_1y + k_1^2 = r_1^2 $$
    $$ C_2: (x-h_2)^2 + (y-k_2)^2 = r_2^2 \implies x^2 - 2h_2x + h_2^2 + y^2 - 2k_2y + k_2^2 = r_2^2 $$
2.  Subtracting the second expanded equation from the first causes the $x^2$ and $y^2$ terms to cancel out, leaving a linear equation:
    $$ 2(h_2 - h_1)x + 2(k_2 - k_1)y + (h_1^2 - h_2^2 + k_1^2 - k_2^2 + r_2^2 - r_1^2) = 0 $$
    This is the equation of the radical axis, a line that passes through the intersection points of the two circles.
3.  The problem is now reduced to finding the intersection of this line with either of the original circles, which is a Line-Circle intersection problem.

---

## 3. Perpendicular Line Mathematics

To find the coordinates of the "foot" of the perpendicular from a point $P_0(x_0, y_0)$ to a line $ax + by + c = 0$, we find the point $P'(x', y')$ on the line that is closest to $P_0$.

The vector from $P'$ to $P_0$, which is $\vec{P'P_0} = \langle x_0 - x', y_0 - y' \rangle$, must be parallel to the line's normal vector $\vec{n} = \langle a, b \rangle$. This means $\vec{P_0P'}$ can be expressed as a scalar multiple of the normal vector.

Let $k$ be a scalar. The point $P'$ can be expressed parametrically from $P_0$ along the normal vector direction:
$$ x' = x_0 - ak $$
$$ y' = y_0 - bk $$
Since $P'(x', y')$ must lie on the line, it satisfies the line's equation:
$$ a(x_0 - ak) + b(y_0 - bk) + c = 0 $$
Solving for the scalar $k$:
$$ ax_0 - a^2k + by_0 - b^2k + c = 0 $$
$$ ax_0 + by_0 + c = k(a^2 + b^2) $$
$$ k = \frac{ax_0 + by_0 + c}{a^2 + b^2} $$
Finally, we substitute this value of $k$ back into the expressions for $x'$ and $y'$ to get the coordinates of the foot of the perpendicular.

---

## 4. Transformation Mathematics

Geometric transformations change the position, orientation, or size of an object.

### Translation
Translation moves every point of an object by the same amount in a given direction. To translate a point $P(x, y)$ by a vector $\vec{v} = \langle dx, dy \rangle$ to a new point $P'(x', y')$, we perform simple vector addition:
$$ x' = x + dx $$
$$ y' = y + dy $$

### Scaling
Scaling resizes an object by a factor $S$ relative to a fixed origin point $O(o_x, o_y)$. The transformation for a point $P(x, y)$ is:
1.  Translate the system so the origin $O$ is at $(0,0)$. The point becomes $P_{rel} = (x - o_x, y - o_y)$.
2.  Apply the scaling: $P'_{rel} = (S \cdot (x - o_x), S \cdot (y - o_y))$.
3.  Translate the system back to the original origin.
The complete formulas are:
$$ x' = o_x + S \cdot (x - o_x) $$
$$ y' = o_y + S \cdot (y - o_y) $$

### Rotation
Rotation turns an object around a fixed origin point $O(o_x, o_y)$ by an angle $\theta$. The process involves translating to the origin, rotating, and translating back.

The core rotation of a point $(x_{rel}, y_{rel})$ around $(0,0)$ is performed using a 2D rotation matrix:
$$
\begin{bmatrix} x'_{rel} \\ y'_{rel} \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} x_{rel} \\ y_{rel} \end{bmatrix}
$$
This gives the equations:
$$ x'_{rel} = x_{rel}\cos\theta - y_{rel}\sin\theta $$
$$ y'_{rel} = x_{rel}\sin\theta + y_{rel}\cos\theta $$
Combining this with the translations for an arbitrary origin $O(o_x, o_y)$ gives the final formulas for rotating a point $P(x,y)$:
$$ x' = o_x + (x - o_x)\cos\theta - (y - o_y)\sin\theta $$
$$ y' = o_y + (x - o_x)\sin\theta + (y - o_y)\cos\theta $$
> **Note**: For these formulas to work with standard math libraries (like Python's `math` module), the angle $\theta$ must be in **radians**.

---
# [HOMEWORK 8](https://github.com/dy546/_cm/blob/5963b7e95ce45df62ca20bb7f0d7486980e5fa9b/homework/information_theory_and_coding.py)

All copied from GEMINI without modification

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

---
# [HOMEWORK 9](https://github.com/dy546/_cm/blob/5963b7e95ce45df62ca20bb7f0d7486980e5fa9b/homework/linear_algebra.py)

All copied from GEMINI without modification

## 1. Core Definitions: Linearity, Algebra, and Space

### What does "Linear" refer to in Linear Algebra? Why is it called "Algebra"?

* **Linearity:** Refers to a function or operation that satisfies two core properties:
    1.  **Additivity:** $f(x + y) = f(x) + f(y)$
    2.  **Homogeneity (Scaling):** $f(ax) = a \cdot f(x)$
    * **Intuitive Understanding:** In a "linear" world, there are only straight lines and planes, no curves. If the input doubles, the output doubles exactly.
* **Algebra:** Refers to the study of mathematical symbols and the rules for manipulating these symbols.
* **Summary:** Linear Algebra uses the symbols and rules of algebra to study linear spaces and linear transformations.

### What is a "Space" in mathematics? Why is a "Vector Space" referred to as a space?

* **Space:** In mathematics, a space refers to a **set** combined with a **structure (rules)** defined on that set.
* **Vector Space:**
    * It is a set composed of "vectors".
    * **Rules (Closure):** No matter how you add or scale elements within this space, the result **remains inside the space** (it doesn't "escape"). This is why it is called a "space"—it is a self-contained playground.

---

## 2. Matrices and Geometric Transformations

### What is the relationship between matrices and vectors? What is the significance represented by a matrix?

* **Relationship:** A matrix is the **"verb,"** and a vector is the **"noun."**
    * Vector $x$ represents data or a state.
    * Matrix $A$ represents a function or transformation.
    * $Ax = b$ means: Matrix $A$ acts on vector $x$, transforming it into $b$.
* **Significance of a Matrix:**
    * **Mapping:** Describes how space is distorted (rotation, scaling, shearing).
    * **Data Table:** Simply stores data (like an Excel spreadsheet).

### How can matrices be used to represent "translation, scaling, and rotation" operations in 2D/3D geometry?

* **Scaling and Rotation:** These are standard linear transformations where the origin remains fixed. They can be represented by $2\times2$ (2D) or $3\times3$ (3D) matrices.
* **Translation:** This is **not** a linear transformation (because the origin $0$ moves, violating $f(0)=0$).
* **Homogeneous Coordinates:** To solve the translation problem, we must add a dimension (2D becomes 3D, 3D becomes 4D).
    * For example, a 2D translation $(dx, dy)$ is represented by a $3\times3$ matrix:
    $$
    \begin{bmatrix} 1 & 0 & dx \\ 0 & 1 & dy \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix} = \begin{bmatrix} x+dx \\ y+dy \\ 1 \end{bmatrix}
    $$

---

## 3. Determinant

### Meaning and Calculation of the Determinant

* **Geometric Meaning:** The volume scaling factor after the matrix transformation.
    * $\det(A) = 2$: The volume expands by two times.
    * $\det(A) = 0$: The volume is flattened to zero (dimensionality reduction), indicating the matrix is **singular** (non-invertible).
    * **Negative Sign:** Indicates the orientation of the space has been flipped (like a mirror image).
* **Recursive Formula (Laplace Expansion):** Expanding along a specific row or column, breaking the large matrix into the sum of determinants of smaller sub-matrices.
* **Calculation via Diagonalization:** If $A$ is diagonalizable, $\det(A)$ equals the product of all eigenvalues ($\lambda$).
    $$\det(A) = \prod \lambda_i$$
* **Calculation via LU Decomposition:**
    * $A = LU$ (Lower triangular $\times$ Upper triangular).
    * $\det(A) = \det(L) \cdot \det(U)$.
    * Because the determinant of a triangular matrix is the product of its diagonal elements, and usually $\det(L)=1$, then $\det(A) = \prod (\text{diag}(U))$. This is one of the fastest ways for computers to calculate determinants.

---

## 4. Matrix Decomposition

### Eigenvalues and Eigenvectors

* **Meaning:** When matrix $A$ acts on certain specific vectors $v$, the **direction** of these vectors remains unchanged; only their **length** stretches or shrinks by a factor of $\lambda$.
* **Formula:** $Av = \lambda v$
* **Physical Meaning:** The "natural frequencies" or "principal axes" of a system.
* **Uses:** Solving differential equations, analyzing system stability, image compression, Google PageRank.

### QR Decomposition and Eigenvalue Iteration

* **QR Decomposition:** Decomposing matrix $A$ into an orthogonal matrix $Q$ and an upper triangular matrix $R$.
    $$A = QR$$
* **Finding Eigenvalues (QR Algorithm):**
    * Iteratively perform: $A_0 = A$. Decompose $A_k = Q_k R_k$, then set $A_{k+1} = R_k Q_k$.
    * After multiple iterations, $A_k$ converges to an upper triangular matrix (or Schur form), where the diagonal elements are the eigenvalues.

### SVD (Singular Value Decomposition) and PCA

* **What is SVD:** A "generalized version" of eigenvalue decomposition. Eigenvalue decomposition only applies to square matrices, while SVD applies to matrices of any shape.
    $$A = U \Sigma V^T$$
* **Geometric Meaning:** Rotation ($V^T$) $\to$ Axis Scaling ($\Sigma$) $\to$ Rotation ($U$).
* **Relationship with Eigenvalues:**
    * The singular values ($\sigma$) of $A$ are the square roots of the eigenvalues ($\lambda$) of $A^T A$ (i.e., $\sigma = \sqrt{\lambda}$).
* **PCA (Principal Component Analysis):**
    * A dimensionality reduction technique aimed at finding the directions with the largest data **variance**.
* **Relationship:** When performing SVD on a data matrix, $V$ (the right singular vectors) represents the **principal component directions** of PCA, and $\Sigma$ (singular values) represents the magnitude of the variance.

# [HOMEWORK 10](https://github.com/dy546/_cm/blob/0c20db85417a868cc636d921166218fa3ec08e8c/homework/hw10.py)

All copied from GEMINI without modification

To implement this in Python, we must bridge the gap between the Continuous Fourier Transform (CFT)
(shown in the math formulas in your image) and the Discrete Fourier Transform (DFT) (which computers use).

1. From Continuous to Discrete Computers cannot process infinite integrals or continuous functions. 
Instead, we use lists of numbers (discrete samples).
    - The integral $\int$ becomes a summation $\sum$.
    - The continuous time $x$ becomes a discrete index $n$.
    - The continuous frequency $\omega$ becomes a discrete frequency index $k$.
2. The Euler Formula The core of the calculation involves the complex exponential, which we calculate using Euler's formula:
    $$e^{-ix} = \cos(x) - i\sin(x)$$
In Python, we use the complex type or the cmath module to handle the imaginary unit $i$ (written as 1j in Python).
3. The Discrete Formulas Since we cannot use the standard FFT packages, we will implement the summation loops manually.

    - DFT Equation (Forward):
        $$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-i \frac{2\pi}{N} k n}$$
    - IDFT Equation (Inverse):
        $$x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] \cdot e^{i \frac{2\pi}{N} k n}$$

> [!NOTE]
> The $1/2\pi$ in your continuous formula is represented by the $1/N$ normalization factor in the discrete domain) 

# [HOMEWORK 11](https://github.com/dy546/_cm/blob/0c20db85417a868cc636d921166218fa3ec08e8c/homework/hw11.py)

All Copied From Gemini Without Modification

1. Mathematical Foundation
The logic is based on the Characteristic Equation method for solving Homogeneous Linear ODEs with constant coefficients:
$$a_n y^{(n)} + \dots + a_1 y' + a_0 y = 0$$
We transform this into a polynomial equation:
$$a_n \lambda^n + \dots + a_1 \lambda + a_0 = 0$$
The form of the solution depends entirely on the roots $\lambda$ of this polynomial.

2. Why Use Numerical Tolerance (tol=1e-5)?
This is the most critical part of the code. In your original execution log, the output was
messy because standard root-finding algorithms (like numpy.roots which uses the eigenvalues 
of the companion matrix) are numerical approximations.

    - The Problem: For the equation $(x-2)^2=0$, the computer might find roots like 2.0000000001 and 1.9999999999.
        - A naive program sees these as two distinct real roots.
        - Result: $C_1 e^{2.000001x} + C_2 e^{1.99999x}$ (Incorrect).

    - The Solution:
        - I implemented a group_roots function.
        - It compares roots. If $|r_1 - r_2| < \epsilon$, they are treated as the same root with a multiplicity count.
        - Result: Root 2 with count=2.
        - Formula applied: $C_1 e^{2x} + C_2 x e^{2x}$ (Correct).

3. Handling Complex Roots
Standard solvers return complex roots in pairs (e.g., $0+2j$ and $0-2j$).
    - Filtering: The code iterates through groups. If the imaginary part beta > 0, it triggers the sine/cosine generation.
    - Ignoring Conjugates: If beta < 0, the code skips it, because the term with beta > 0 has already generated the 
necessary $\cos(\beta x)$ and $\sin(\beta x)$ pair for the solution.
    - Purely Imaginary: The code checks if the real part alpha is close to 0. If so, it suppresses the $e^{0x}$ term 
to clean up the output (just $\cos(2x)$ instead of $e^{0x}\cos(2x)$).

4. String Formatting Logic
To ensure the output looks like a human wrote it (matches your "Expected Solution"), specific formatting rules were applied:

    - 1x vs x: If the coefficient is 1, do not print "1".
    - e^(0x): If the exponent is 0, remove the exponential term entirely.
    - Floating Point Display: Used {:.5g} to format numbers nicely (e.g., turns 2.00000004 into 2, but keeps 2.5 as 2.5).

5. Algorithm Flowchart
    - Input: Coefficient List [1, -4, 4].
    - NumPy: Find roots $\to$ [2.+0.j, 2.+0.j].
    - Grouping: Detect these are within tolerance $\to$ {'value': 2, 'count': 2}.
    - Generation:Count 0: $C_1 e^{2x}$Count 1: $C_2 x e^{2x}$
    - Output: Combine strings $\to$ "y(x) = C_1e^(2x) + C_2xe^(2x)".
    
    
