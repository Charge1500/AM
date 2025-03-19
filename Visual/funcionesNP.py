import re

def add_np_prefix(func_str: str) -> str:
    # Reemplazar funciones que llevan paréntesis
    funciones = ['sin', 'cos', 'tan', 'exp', 'log', 'log10', 'log2', 
                'sqrt', 'arcsin', 'arccos', 'arctan', 'power']
    for func in funciones:
        func_str = func_str.replace(f"{func}(", f"np.{func}(")
    
    # Reemplazar constantes (manejo con regex para evitar reemplazos parciales)
    constantes = {'pi': 'np.pi', 'e': 'np.e'}
    for const, np_const in constantes.items():
        func_str = re.sub(rf'\b{const}\b', np_const, func_str)
    
    # Reemplazar operadores no estándar
    func_str = func_str.replace('^', '**')
    
    return func_str