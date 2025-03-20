import numpy as np
import re

expo = False
exp = None
func_retorno = None
def add_np_prefix(func_str: str) -> str:
    global expo
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
    if re.match(patron, func_str):
        while True:
            global sustituido
            sustituido = False
            
            def reemplazo(match):
                global sustituido
                global base 
                global exp_str
                global exp
                global func_retorno
                sustituido = True
                base = match.group(1)
                exp_str = match.group(2)
                func_retorno = f'(np.sign({base})) * (np.abs({base}) ** ({exp_str}))'
                
                try:
                    global exp
                    exp = eval(exp_str)
                    global expo
                    if validate_expo(exp):
                        expo = True
                    else:
                        expo = False
                except:
                    None
                
                return func_retorno
            
            # Sustituir
            nueva_func_str = re.sub(patron, reemplazo, func_str)

            if not sustituido:
                break
                
            func_str = nueva_func_str
            
            #print(expo)

        return func_str
    
def convertir_constantes(expresion: str) -> str:
    expresion = expresion.replace('pi', str(np.pi))
    expresion = expresion.replace('euler', str(np.e))
    expresion = expresion.replace('e', str(np.e))  
    return expresion

def evaluar_intervalo(intervalo: str) -> float:
    try:
        intervalo = convertir_constantes(intervalo)
        
        return float(eval(intervalo, {'__builtins__': None}))
        
    except Exception as e:
        raise ValueError(f"Error en intervalo: {str(e)}")

def validate_expo(e):
    global base
    global exp_str
    try:
        # Raiz cuadrada
        if (-1) ** float((1/float(e))) >= 0 :
            return True
        print("a")
        return False
    except:
        global func_retorno
        # Elevar al cuadrado
        func_retorno = f'{base} ** {exp_str}'
        return False

def return_expo():
    global expo
    print(expo)
    return expo



