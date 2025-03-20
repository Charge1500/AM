import numpy as np

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

def raiz_impar(x, n):
    return np.sign(x) * np.abs(x) ** (1/n)
