import numpy as np
from scipy.linalg import lu, qr, svd, eig

np.set_printoptions(precision=4, suppress=True)

# 準備一個範例矩陣
A = np.array([[4., 1., -1.],
              [2., 5., -2.],
              [1., 1., 2.]])

print(f"原始矩陣 A:\n{A}\n")
print("-" * 30)

# ==========================================
# 1. 寫程式用遞迴的方式計算行列式 (Recursive Determinant)
# ==========================================
def recursive_det(matrix):
    n = len(matrix)
    # Base case: 2x2 矩陣
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det_val = 0
    for c in range(n):
        # 建立子矩陣 (移除第 0 列，第 c 行)
        sub_matrix = np.delete(np.delete(matrix, 0, axis=0), c, axis=1)
        # Laplace 展開公式: (-1)^col * element * sub_det
        det_val += ((-1) ** c) * matrix[0][c] * recursive_det(sub_matrix)
    return det_val

print("1. 遞迴計算行列式:")
print(f"Recursive Det: {recursive_det(A)}")
print(f"Numpy Det:     {np.linalg.det(A)}") # 驗證
print("-" * 30)

# ==========================================
# 2. 寫程式做 LU 分解後，再計算行列式
# ==========================================
def det_via_lu(matrix):
    # 使用 scipy 做 P(置換), L, U 分解
    P, L, U = lu(matrix)
    # Det(A) = Det(P) * Det(L) * Det(U)
    # Det(L) 通常為 1 (對角線為1)
    # Det(U) 為對角線乘積
    # Det(P) 取決於交換次數 (1 或 -1)
    
    det_u = np.prod(np.diag(U))
    det_p = np.linalg.det(P) # P 是正交矩陣，行列式為 1 或 -1
    
    return det_p * det_u

print("2. 透過 LU 分解計算行列式:")
print(f"LU Det: {det_via_lu(A)}")
print("-" * 30)

# ==========================================
# 3. 驗證 LU, 特徵值, SVD 分解後，相乘可還原
# ==========================================
print("3. 驗證矩陣分解還原:")

# A. LU 分解
P, L, U = lu(A)
A_lu = P @ L @ U
print(f"LU 還原誤差: {np.linalg.norm(A - A_lu)}")

# B. 特徵值分解 (A = V * Diag(lambda) * V^-1)
vals, vecs = eig(A)
D = np.diag(vals)
V = vecs
V_inv = np.linalg.inv(V)
A_eig = V @ D @ V_inv
print(f"Eig 還原誤差: {np.linalg.norm(A - A_eig)}")

# C. SVD 分解 (A = U * Sigma * Vt)
U_svd, S, Vt = svd(A)
Sigma = np.zeros_like(A)
np.fill_diagonal(Sigma, S)
A_svd = U_svd @ Sigma @ Vt
print(f"SVD 還原誤差: {np.linalg.norm(A - A_svd)}")
print("-" * 30)

# ==========================================
# 4. 寫程式用特徵值分解來做 SVD (從定義出發)
# ==========================================
# SVD: A = U S V.T
# V 是 A.T @ A 的特徵向量
# S (Singular values) 是 A.T @ A 的特徵值的平方根
# U 可以由 A @ V @ S_inv 求得
print("4. 手刻 SVD (透過特徵值分解):")

ATA = A.T @ A
eig_vals, eig_vecs = np.linalg.eig(ATA)

# 排序特徵值與特徵向量 (從大到小)
sorted_indices = np.argsort(eig_vals)[::-1]
eig_vals = eig_vals[sorted_indices]
V_calculated = eig_vecs[:, sorted_indices]

# 計算奇異值 Sigma
singular_values = np.sqrt(np.abs(eig_vals)) # 取 abs 避免極小負值誤差

# 計算 U ( U = A * V / Sigma )
# 注意：這裡只適用於方陣且滿秩的情況，一般情況需更嚴謹處理
Sigma_mat = np.diag(singular_values)
U_calculated = A @ V_calculated @ np.linalg.inv(Sigma_mat)

print("計算出的奇異值 (Sigma):", singular_values)
print("標準函式庫奇異值:      ", S)
# 注意：U 和 V 的符號可能與標準庫不同（這是數學上允許的，只要 U 和 V 同時變號）
print("-" * 30)

# ==========================================
# 5. 寫程式做 PCA 主成份分析
# ==========================================
print("5. PCA 實作:")
# 假設有 5 筆數據，每筆數據是 3 維 (5x3)
Data = np.array([
    [2.5, 2.4, 0.5],
    [0.5, 0.7, 0.3],
    [2.2, 2.9, 0.4],
    [1.9, 2.2, 0.2],
    [3.1, 3.0, 0.6]
])

# Step 1: 中心化 (Centering) - 減去平均值
mean_vec = np.mean(Data, axis=0)
Data_centered = Data - mean_vec

# Step 2: 計算協方差矩陣 (Covariance Matrix)
# rowvar=False 代表每一列是一筆數據
cov_mat = np.cov(Data_centered, rowvar=False)

# Step 3: 對協方差矩陣做特徵值分解
eig_vals, eig_vecs = np.linalg.eigh(cov_mat) # eigh 用於對稱矩陣，更穩

# Step 4: 排序並選取主成分 (取前 2 個)
sorted_idx = np.argsort(eig_vals)[::-1]
top_k = 2
components = eig_vecs[:, sorted_idx][:, :top_k]

print(f"主成分方向 (Eigenvectors):\n{components}")

# Step 5: 投影數據到新空間
projected_data = Data_centered @ components
print(f"降維後的數據 (5x2):\n{projected_data}")