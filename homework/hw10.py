import numpy as np
import matplotlib.pyplot as plt

# We use numpy only for array management (storing data) and pi.
# We will NOT use numpy.fft or any Fourier packages.

def dft(x):
    """
    Computes the Discrete Fourier Transform (Forward).
    Corresponds to: F(omega) = integral f(x) * e^(-i * omega * x)
    """
    N = len(x)
    # Create an empty array of complex numbers for the result
    X = np.zeros(N, dtype=complex)
    
    # Nested loops to simulate the summation (The O(N^2) algorithm)
    for k in range(N):  # For each frequency component k
        sum_val = 0.0 + 0.0j
        for n in range(N):  # For each time sample n
            # The angle theta = -2 * pi * k * n / N
            theta = -2 * np.pi * k * n / N
            
            # e^(theta) = cos(theta) + i*sin(theta)
            # This is the "kernel" of the transform
            complex_exponential = np.cos(theta) + 1j * np.sin(theta)
            
            # Summation
            sum_val += x[n] * complex_exponential
            
        X[k] = sum_val
        
    return X

def idft(X):
    """
    Computes the Inverse Discrete Fourier Transform.
    Corresponds to: f(x) = (1/2pi) * integral F(omega) * e^(i * omega * x)
    """
    N = len(X)
    x_reconstructed = np.zeros(N, dtype=complex)
    
    for n in range(N):
        sum_val = 0.0 + 0.0j
        for k in range(N):
            # The angle theta = 2 * pi * k * n / N (Positive for Inverse)
            theta = 2 * np.pi * k * n / N
            
            # e^(theta)
            complex_exponential = np.cos(theta) + 1j * np.sin(theta)
            
            sum_val += X[k] * complex_exponential
            
        # Apply the normalization factor (1/N)
        # This matches the 1/2pi factor in the continuous formula context
        x_reconstructed[n] = sum_val / N
        
    return x_reconstructed

# --- 3. Verification Step ---

# A. Generate a sample function f(x)
# Let's create a signal composed of two sine waves
N = 64  # Number of samples
t = np.linspace(0, 1, N) # Time vector
# Signal: 1Hz sine wave + 5Hz sine wave
f_original = np.sin(2 * np.pi * 1 * t) + 0.5 * np.sin(2 * np.pi * 5 * t)

print(f"Original Signal (First 5 samples):\n{f_original[:5]}\n")

# B. Perform Forward Transform: dft(f)
F_transformed = dft(f_original)
print(f"Transformed Frequency Data (First 5 samples):\n{F_transformed[:5]}\n")

# C. Perform Inverse Transform: idft(F)
f_recovered = idft(F_transformed)

# We take the real part because the original signal was real.
# (Small imaginary parts might exist due to floating point rounding errors)
f_recovered_real = np.real(f_recovered)
print(f"Recovered Signal (First 5 samples):\n{f_recovered_real[:5]}\n")

# D. Verify equality
# Check if the difference is extremely small (close to zero)
mse = np.mean((f_original - f_recovered_real)**2)
is_close = np.allclose(f_original, f_recovered_real)

print("-" * 30)
print(f"Mean Squared Error: {mse:.20f}")
if is_close:
    print("VERIFICATION SUCCESSFUL: The recovered function matches the original function.")
else:
    print("VERIFICATION FAILED: The functions do not match.")

# Optional: Visualization (if running in a local environment)
#  would be generated here in a real notebook
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t, f_original, 'b-', label='Original f(x)', linewidth=2)
plt.plot(t, f_recovered_real, 'r--', label='Recovered f(x) via IDFT', linewidth=2)
plt.legend()
plt.title("Original vs Recovered Signal")

plt.subplot(2, 1, 2)
plt.stem(np.abs(F_transformed))
plt.title("Magnitude of F(omega) [DFT]")
plt.tight_layout()
plt.show()
