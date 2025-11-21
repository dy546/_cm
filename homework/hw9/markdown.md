# HOMEWORK 9

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