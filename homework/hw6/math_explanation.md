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