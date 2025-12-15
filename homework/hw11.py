import numpy as np

def solve_ode_general(coefficients):
    """
    Solves a homogeneous linear ODE with constant coefficients.
    Equation: a_n y^(n) + ... + a_1 y' + a_0 y = 0
    """
    # 1. Solve the characteristic equation (polynomial)
    # Roots are returned as complex floats (e.g., 1+0j, 0+2j)
    raw_roots = np.roots(coefficients)
    
    # 2. Group roots with a tolerance to handle floating point noise.
    # We treat 1.999999999 and 2.000000001 as the same root (2).
    # We treat 1e-15j as 0 (real).
    groups = group_roots(raw_roots)
    
    # 3. Construct the solution string
    terms = []
    c_index = 1  # Counter for constants C_1, C_2, etc.
    
    # Sort groups by real part then imaginary part for consistent output order
    groups.sort(key=lambda x: (x['value'].real, abs(x['value'].imag)))
    
    for group in groups:
        root = group['value']
        count = group['count']
        
        alpha = root.real
        beta = root.imag
        
        # Determine if it's a Real root or Complex Pair
        # If beta is effectively 0, treat as real.
        if np.isclose(beta, 0, atol=1e-5):
            # --- Case 1: Real Roots (Distinct or Repeated) ---
            for k in range(count):
                # Term structure: C_n * x^k * e^(alpha*x)
                term_str = format_real_term(c_index, k, alpha)
                terms.append(term_str)
                c_index += 1
        elif beta > 0:
            # --- Case 2: Complex Conjugate Roots (Distinct or Repeated) ---
            # We only process the positive beta (alpha + beta*i).
            # The negative beta is strictly conjugate and covered by the same formula.
            for k in range(count):
                # Terms: C_n * x^k * e^(ax)cos(bx) + C_m * x^k * e^(ax)sin(bx)
                term_cos = format_complex_term(c_index, k, alpha, beta, "cos")
                term_sin = format_complex_term(c_index + 1, k, alpha, beta, "sin")
                terms.append(term_cos)
                terms.append(term_sin)
                c_index += 2
        else:
            # If beta < 0, we skip it because it was handled by the positive partner.
            continue

    # Join all terms with " + "
    solution = " + ".join(terms)
    
    # Clean up formatting: "+ -" becomes "- "
    solution = solution.replace("+ -", "- ")
    
    return f"y(x) = {solution}"

def group_roots(roots, tol=1e-5):
    """
    Groups roots that are numerically close to each other.
    Returns a list of dicts: [{'value': representative_root, 'count': multiplicity}, ...]
    """
    groups = []
    used_indices = set()
    
    for i, r1 in enumerate(roots):
        if i in used_indices:
            continue
            
        current_group = [r1]
        used_indices.add(i)
        
        for j, r2 in enumerate(roots):
            if j not in used_indices and j > i: # j > i ensures we don't look back
                if np.isclose(r1, r2, atol=tol):
                    current_group.append(r2)
                    used_indices.add(j)
        
        # Calculate average value for the group to minimize error
        avg_val = np.mean(current_group)
        groups.append({'value': avg_val, 'count': len(current_group)})
        
    return groups

def format_real_term(c_idx, power_x, alpha):
    """Formats C_i x^k e^(ax)"""
    # 1. Constant
    term = f"C_{c_idx}"
    
    # 2. x term (multiplicity)
    if power_x == 1:
        term += "x"
    elif power_x > 1:
        term += f"x^{power_x}"
        
    # 3. Exponential term
    if np.isclose(alpha, 0, atol=1e-5):
        pass # e^0 is 1, so don't add string
    elif np.isclose(alpha, 1, atol=1e-5):
        term += "e^(x)"
    else:
        # Clean float (e.g., 2.0 -> 2)
        alpha_str = f"{alpha:.5g}" 
        term += f"e^({alpha_str}x)"
        
    return term

def format_complex_term(c_idx, power_x, alpha, beta, trig_type):
    """Formats C_i x^k e^(ax) [cos|sin](bx)"""
    term = f"C_{c_idx}"
    
    # x term
    if power_x == 1:
        term += "x"
    elif power_x > 1:
        term += f"x^{power_x}"
    
    # Exponential term (e^ax)
    if not np.isclose(alpha, 0, atol=1e-5):
        alpha_str = f"{alpha:.5g}"
        term += f"e^({alpha_str}x)"
        
    # Trig term
    beta_str = f"{beta:.5g}"
    if np.isclose(beta, 1, atol=1e-5):
        term += f"{trig_type}(x)"
    else:
        term += f"{trig_type}({beta_str}x)"
        
    return term

# --- MAIN TESTING PROGRAM (From your request) ---

if __name__ == "__main__":
    # Example 1: Real Distinct
    print("--- Example 1: Real Distinct Roots ---")
    coeffs1 = [1, -3, 2] # r = 1, 2
    print(f"Coefficients: {coeffs1}")
    print(solve_ode_general(coeffs1))

    # Example 2: Real Repeated
    print("\n--- Example 2: Real Repeated Roots ---")
    coeffs2 = [1, -4, 4] # r = 2, 2
    print(f"Coefficients: {coeffs2}")
    print(solve_ode_general(coeffs2))

    # Example 3: Complex Conjugate
    print("\n--- Example 3: Complex Conjugate Roots ---")
    coeffs3 = [1, 0, 4] # r = +/- 2i
    print(f"Coefficients: {coeffs3}")
    print(solve_ode_general(coeffs3))

    # Example 4: Repeated Complex
    print("\n--- Example 4: Repeated Complex Roots ---")
    # (D^2 + 1)^2 -> r = i, i, -i, -i
    coeffs4 = [1, 0, 2, 0, 1] 
    print(f"Coefficients: {coeffs4}")
    print(solve_ode_general(coeffs4))

    # Example 5: High Order Repeated
    print("\n--- Example 5: High Order Repeated Roots ---")
    # (r - 2)^3 -> r = 2, 2, 2
    coeffs5 = [1, -6, 12, -8]
    print(f"Coefficients: {coeffs5}")
    print(solve_ode_general(coeffs5))
