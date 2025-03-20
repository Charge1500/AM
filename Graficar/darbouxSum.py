import numpy as np

def darboux_sums(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    dx = (b - a) / n
    lower_sum = 0
    upper_sum = 0
    for i in range(n):
        x_left = x[i]
        x_right = x[i + 1]
        m_i = min(f(np.linspace(x_left, x_right, 100)))
        M_i = max(f(np.linspace(x_left, x_right, 100)))
        lower_sum += m_i * dx
        upper_sum += M_i * dx
    return lower_sum, upper_sum, x