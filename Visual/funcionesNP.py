def add_np_prefix(func_str):
    math_functions = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'arcsin', 'arccos', 'arctan']
    for func in math_functions:
        func_str = func_str.replace(f"{func}(", f"np.{func}(")
    return func_str