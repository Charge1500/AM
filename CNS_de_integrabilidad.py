import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox
from scipy.integrate import quad
import warnings

def darboax_sums(f, a, b, n):  
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

def update_animation(frame):
    n = frame + 1  
    if(frame == frames - 1):
        update_last_frame()
    else:
        update_left_plots(n) 
    
    plt.draw() 

def update_left_plots(n):
    for i in [1, 3]:  
        plt.subplot(2, 2, i) 
        plt.cla()  
    
    lower_sum_main, upper_sum_main, x_main = darboax_sums(f, a, b, n)
    
    plt.subplot(2, 2, 1)  
    plot_darboax(f, a, b, n, x_main, lower_sum_main, 'green', 'Suma Inferior (Intervalo Completo)') 
    
    plt.subplot(2, 2, 3)  
    plot_darboax(f, a, b, n, x_main, upper_sum_main, 'red', 'Suma Superior (Intervalo Completo)')

def update_last_frame():
    for i in [1, 3]:  
        plt.subplot(2, 2, i)
        plt.cla()  
    
    integral_value, _ = quad(f, a, b)
    
    plt.subplot(2, 2, 1)  
    plot_area_under_curve(f, a, b, 'green', f'Área bajo la curva (Suma Inferior = {integral_value:.4f})')
    
    plt.subplot(2, 2, 3)  
    plot_area_under_curve(f, a, b, 'red', f'Área bajo la curva (Suma Superior = {integral_value:.4f})')

def plot_area_under_curve(f, a, b, color, title):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    plt.plot(x_vals, y_vals, 'b-', label='Función $f(x)$')
    plt.fill_between(x_vals, 0, y_vals, color=color, alpha=0.5, label='Área bajo la curva')
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid()

def update_right_plots(val):
    n = int(slider.val)
    update_right_plots_impl(n)

def update_right_plots_impl(n):
    for i in [2, 4]:  
        plt.subplot(2, 2, i) 
        plt.cla()  

    lower_sum_sub, upper_sum_sub, x_sub = darboax_sums(f, c, d, n)    
    
    plt.subplot(2, 2, 2)  
    plot_darboax(f, c, d, n, x_sub, lower_sum_sub, 'green', 'Suma Inferior (Subintervalo)')
    
    plt.subplot(2, 2, 4) 
    plot_darboax(f, c, d, n, x_sub, upper_sum_sub, 'red', 'Suma Superior (Subintervalo)')
    
    plt.draw()

def plot_darboax(f, a, b, n, x_partition, sum_value, color, title):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals, 'b-', label='Función $f(x)$')

    is_lower = color == 'green' 
    
    for i in range(len(x_partition) - 1):
        x_left = x_partition[i]
        x_right = x_partition[i + 1]
        
        values = f(np.linspace(x_left, x_right, 100))
        height = min(values) if is_lower else max(values)
        
        plt.fill_between([x_left, x_right], [0, 0], [height, height], 
                        color=color, alpha=0.5, 
                        label='Suma Inferior' if (i == 0 and is_lower) else 
                              'Suma Superior' if (i == 0 and not is_lower) else "")

    plt.title(f'{title} (n = {n})\nSuma = {sum_value:.4f}')
    plt.xlabel('x') 
    plt.ylabel('y')
    plt.legend() 
    plt.grid() 

def add_np_prefix(func_str):
    math_functions = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'arcsin', 'arccos', 'arctan']
    for func in math_functions:
        func_str = func_str.replace(f"{func}(", f"np.{func}(")
    return func_str

def submit(text):
    global f, a, b, c, d
    try:
        func_str = func_textbox.text
        a = float(interval_a_textbox.text)
        b = float(interval_b_textbox.text)
        
        if b <= a:
            error_textbox.set_val("Error: 'b' debe ser mayor que 'a'.")
            return
        if (b - a) > 25:
            error_textbox.set_val("Error: El intervalo (b - a) debe ser <= 25.")
            return
        
        if 'x' not in func_str:
            error_textbox.set_val("Error: La función debe estar evaluada en 'x'.")
            return
        
        func_str = add_np_prefix(func_str)
        
        try:
            test_x = 1.0
            test_result = eval(func_str, {'np': np, 'x': test_x})
            if not isinstance(test_result, (int, float)):
                error_textbox.set_val("Error: Función no válida.")
                return
        except Exception as e:
            error_textbox.set_val("Error: Función no válida.")
            return
        
        f = lambda x: eval(func_str, {'np': np, 'x': x})
        
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("error")  
                integral_value, _ = quad(f, a, b)
        except Exception as e:
            error_textbox.set_val("Error: La función no es integrable en el intervalo dado.")
            return
        
        c, d = a, b
        
        func_textbox.ax.set_visible(False)
        interval_a_textbox.ax.set_visible(False)
        interval_b_textbox.ax.set_visible(False)
        button.ax.set_visible(False)
        error_textbox.ax.set_visible(False)
        
        plt.subplots_adjust(bottom=0.1, hspace=0.5)
        
        global anim
        anim = FuncAnimation(fig, update_animation, frames=frames, interval=500, repeat=False)
        
        ax_slider = plt.axes([0.6, 0.025, 0.3, 0.03])
        global slider
        slider = Slider(ax_slider, 'Intervalos (n)', 1, 300, valinit=1, valstep=1)
        slider.on_changed(update_right_plots)
        
        update_left_plots(1)
        update_right_plots_impl(1)
        
        plt.draw()
    except ValueError:
        error_textbox.set_val("Error: 'a' y 'b' deben ser números válidos.")
    except Exception as e:
        error_textbox.set_val(f"Error: {e}")

f = lambda x: np.sin(x) 
a, b = 0, 5         
c, d = 0, 5
frames = 51

fig = plt.figure(figsize=(12, 8))
plt.subplots_adjust(bottom=0.4)

ax_func = plt.axes([0.3, 0.6, 0.4, 0.05])
func_textbox = TextBox(ax_func, 'f(x)', initial='sin(x)')

ax_interval_a = plt.axes([0.3, 0.5, 0.18, 0.05])
interval_a_textbox = TextBox(ax_interval_a, 'a', initial='0')

ax_interval_b = plt.axes([0.52, 0.5, 0.18, 0.05])
interval_b_textbox = TextBox(ax_interval_b, 'b', initial='5')

ax_error = plt.axes([0.3, 0.4, 0.4, 0.05])
error_textbox = TextBox(ax_error, 'Mensajes de error', initial='Buen día camarada')
error_textbox.set_active(False)  

ax_button = plt.axes([0.4, 0.3, 0.2, 0.075])
button = Button(ax_button, 'Aceptar')
button.on_clicked(submit)

plt.show()