import numpy as np
import re

def add_np_prefix(func_str: str) -> str:
  
    funciones = ['sin', 'cos', 'tan', 'exp', 'log', 'log10', 'log2', 'sqrt']
    for func in funciones:
        func_str = func_str.replace(f"{func}(", f"np.{func}(")
    func_str = func_str.replace("arcnp.sin(", "np.arcsin(")
    func_str = func_str.replace("arcnp.cos(", "np.arccos(")
    func_str = func_str.replace("arcnp.tan(", "np.arctan(")
    
    constantes = {'pi': 'np.pi', 'e': 'np.e'}
    for const, np_const in constantes.items():
        func_str = re.sub(rf'\b{const}\b', np_const, func_str)
    
    patron = r'power\(((?:[^()]|\(.*?\))+?),\s*((?:[^()]|\(.*?\))+?)\)'
    if re.match(patron,func_str):
        while True:
            nueva_func_str = re.sub(
                patron,
                lambda match: f'(np.sign({match.group(1)})) * (np.abs({match.group(1)}) ** ({match.group(2)}))',
                func_str
            )
            if nueva_func_str == func_str:
                break  # No hay más cambios, salir del bucle
            func_str = nueva_func_str
    
    return func_str
    
def convertir_constantes(expresion: str) -> str:
    # Reemplazar pi → np.pi y euler/e → np.e
    expresion = expresion.replace('pi', str(np.pi))
    expresion = expresion.replace('euler', str(np.e))
    expresion = expresion.replace('e', str(np.e))  # También manejar 'e' como alias de euler
    return expresion

def evaluar_intervalo(intervalo: str) -> float:
    try:
        # Convertir pi y euler a valores numéricos
        intervalo = convertir_constantes(intervalo)
        
        # Evaluar la expresión resultante
        return float(eval(intervalo, {'__builtins__': None}))
        
    except Exception as e:
        raise ValueError(f"Error en intervalo: {str(e)}")