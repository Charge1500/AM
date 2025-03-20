import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from Visual.paleta import COLOR_PALETTE

def plot_darboux(f, a, b, n, x_partition, sum_value, color, title):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    plt.plot(x_vals, y_vals, color=COLOR_PALETTE['text'], linewidth=1.5)
    is_lower = color == COLOR_PALETTE['primary']
    
    for i in range(len(x_partition) - 1):
        x_left = x_partition[i]
        x_right = x_partition[i + 1]
        values = f(np.linspace(x_left, x_right, 100))
        height = min(values) if is_lower else max(values)
        
        plt.fill_between([x_left, x_right], [0, 0], [height, height],
                        color=color, alpha=0.3, edgecolor=color, linewidth=0.5)
    
    plt.title(f'{title}\n(n = {n}, Suma = {sum_value:.4f})', fontsize=10, pad=10)
    plt.grid(alpha=0.5)
    plt.gca().set_facecolor('#FFFFFF')

def plot_area_under_curve(f, a, b, color, title):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    plt.plot(x_vals, y_vals, color=COLOR_PALETTE['text'], linewidth=1.5)
    plt.fill_between(x_vals, 0, y_vals, color=color, alpha=0.3)
    plt.title(title, fontsize=10, pad=10)
    plt.grid(alpha=0.5)
    plt.gca().set_facecolor('#FFFFFF')

def es_integral_propia(f, a, b, puntos_muestra=1000):
    try:
        # Verificar límites finitos
        if np.isinf(a) or np.isinf(b):
            return False
        
        f(a)  # Genera error si no está definida en a
        f(b)  # Genera error si no está definida en b
        puntos = np.linspace(a, b, puntos_muestra)
        for x in puntos:
            if not np.isfinite(f(x)):
                return False
        
        return True
    
    except:
        return False
