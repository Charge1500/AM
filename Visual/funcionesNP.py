import re

def add_np_prefix(func_str: str) -> str:
  
    funciones = ['sin', 'cos', 'tan', 'exp', 'log', 'log10', 'log2', 
                'sqrt', 'arcsin', 'arccos', 'arctan']
    for func in funciones:
        func_str = func_str.replace(f"{func}(", f"np.{func}(")
    
    constantes = {'pi': 'np.pi', 'e': 'np.e'}
    for const, np_const in constantes.items():
        func_str = re.sub(rf'\b{const}\b', np_const, func_str)
    
    func_str = func_str.replace('^', '**')
    
    return func_str