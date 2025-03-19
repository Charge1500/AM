import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox
from matplotlib.patches import FancyBboxPatch
from scipy.integrate import quad
import warnings

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
COLOR_PALETTE = {
    'background': '#F5F5F5',
    'primary': '#4A90E2',
    'secondary': '#2C3E50',
    'error': '#E74C3C',
    'text': '#2C3E50',
    'widget': '#4A90E2',
    'hover': '#357ABD'
}

# Función para calcular las sumas de Darboax
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

# Funciones de actualización
def update_animation(frame):
    n = frame + 1
    if frame == frames - 1:
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
    plot_darboax(f, a, b, n, x_main, lower_sum_main, COLOR_PALETTE['primary'], 'Suma Inferior')
    
    plt.subplot(2, 2, 3)
    plot_darboax(f, a, b, n, x_main, upper_sum_main, COLOR_PALETTE['secondary'], 'Suma Superior')

def update_last_frame():
    for i in [1, 3]:
        plt.subplot(2, 2, i)
        plt.cla()
    
    integral_value, _ = quad(f, a, b)
    
    plt.subplot(2, 2, 1)
    plot_area_under_curve(f, a, b, COLOR_PALETTE['primary'], f'Área Exacta: {integral_value:.4f}')
    
    plt.subplot(2, 2, 3)
    plot_area_under_curve(f, a, b, COLOR_PALETTE['secondary'], f'Área Exacta: {integral_value:.4f}')

def plot_area_under_curve(f, a, b, color, title):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)
    plt.plot(x_vals, y_vals, color=COLOR_PALETTE['text'], linewidth=1.5)
    plt.fill_between(x_vals, 0, y_vals, color=color, alpha=0.3)
    plt.title(title, fontsize=10, pad=10)
    plt.grid(alpha=0.5)
    plt.gca().set_facecolor('#FFFFFF')

def update_right_plots(val):
    n = int(slider.val)
    update_right_plots_impl(n)

def update_right_plots_impl(n):
    for i in [2, 4]:
        plt.subplot(2, 2, i)
        plt.cla()
    
    lower_sum_sub, upper_sum_sub, x_sub = darboax_sums(f, c, d, n)
    
    plt.subplot(2, 2, 2)
    plot_darboax(f, c, d, n, x_sub, lower_sum_sub, COLOR_PALETTE['primary'], 'Suma Inferior (Subintervalo)')
    
    plt.subplot(2, 2, 4)
    plot_darboax(f, c, d, n, x_sub, upper_sum_sub, COLOR_PALETTE['secondary'], 'Suma Superior (Subintervalo)')
    
    plt.draw()

def plot_darboax(f, a, b, n, x_partition, sum_value, color, title):
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
            error_textbox.set_val("Error: 'b' debe ser mayor que 'a'")
            return
        if (b - a) > 25:
            error_textbox.set_val("Intervalo máximo: 25 unidades")
            return
        
        if 'x' not in func_str:
            error_textbox.set_val("La función debe contener 'x'")
            return
        
        func_str = add_np_prefix(func_str)
        
        try:
            test_result = eval(func_str, {'np': np, 'x': 1.0})
            if not isinstance(test_result, (int, float)):
                error_textbox.set_val("Función no válida")
                return
        except:
            error_textbox.set_val("Error en la función")
            return
        
        f = lambda x: eval(func_str, {'np': np, 'x': x})
        
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("error")
                quad(f, a, b)
        except:
            error_textbox.set_val("Función no integrable")
            return
        
        c, d = a, b
        
        for widget in [func_textbox, interval_a_textbox, interval_b_textbox, button]:
            widget.ax.set_visible(False)
        
        plt.subplots_adjust(bottom=0.15, hspace=0.5)
        
        global anim
        anim = FuncAnimation(fig, update_animation, frames=frames, interval=300, repeat=False)
        
        slider_ax = plt.axes([0.3, 0.08, 0.4, 0.03], facecolor=COLOR_PALETTE['background'])
        plt.gca().add_patch(FancyBboxPatch(
            (0,0), 1, 1,
            boxstyle="round,pad=0.1,rounding_size=0.05",
            ec=COLOR_PALETTE['primary'],
            fc=COLOR_PALETTE['background'],
            lw=1
        ))
        global slider
        slider = Slider(
            slider_ax, 'Precisión (n)', 1, 200, 
            valinit=1, valstep=1,
            color=COLOR_PALETTE['primary'],
            handle_style={'facecolor': COLOR_PALETTE['primary'], 'edgecolor': 'white'}
        )
        slider.on_changed(update_right_plots)
        
        update_left_plots(1)
        update_right_plots_impl(1)
        error_textbox.ax.set_visible(False)
        plt.draw()
    except ValueError:
        error_textbox.set_val("Valores inválidos")
    except Exception as e:
        error_textbox.set_val(f"Error: {str(e)}")

# Configuración inicial
f = lambda x: np.sin(x)
a, b = 0, np.pi
c, d = 0, np.pi
frames = 50

# Crear figura
fig = plt.figure(figsize=(12, 8), facecolor=COLOR_PALETTE['background'])
plt.subplots_adjust(bottom=0.4)

# Función para crear widgets
def create_rounded_widget(position, text, initial=''):
    ax = plt.axes(position)
    ax.set_facecolor('none')
    ax.axis('off')
    box = FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle="round,pad=0.1,rounding_size=0.1",
        ec=COLOR_PALETTE['text'],
        fc='white',
        lw=1
    )
    ax.add_patch(box)
    textbox = TextBox(ax, text, initial=initial, 
                     color=COLOR_PALETTE['text'], 
                     hovercolor=COLOR_PALETTE['hover'])
    return textbox

# Widgets de entrada
func_textbox = create_rounded_widget([0.25, 0.75, 0.5, 0.06], 'f(x) = ', 'sin(x)')
interval_a_textbox = create_rounded_widget([0.25, 0.65, 0.2, 0.06], 'a = ', '0')
interval_b_textbox = create_rounded_widget([0.55, 0.65, 0.2, 0.06], 'b = ', '5')

# Botón con bordes redondeados
button_ax = plt.axes([0.4, 0.55, 0.2, 0.07])
button_ax.axis('off')
button_box = FancyBboxPatch(
    (0, 0), 1, 1,
    boxstyle="round,pad=0.1,rounding_size=0.1",
    ec=COLOR_PALETTE['primary'],
    fc=COLOR_PALETTE['primary'],
    lw=1.5
)
button_ax.add_patch(button_box)
button = Button(button_ax, 'CALCULAR', color=COLOR_PALETTE['primary'], 
               hovercolor=COLOR_PALETTE['hover'])
button.label.set_color('white')
button.label.set_fontweight('bold')
button.on_clicked(submit)

# Cuadro de error
error_ax = plt.axes([0.25, 0.45, 0.5, 0.06])
error_ax.axis('off')
error_box = FancyBboxPatch(
    (0, 0), 1, 1,
    boxstyle="round,pad=0.1,rounding_size=0.05",
    ec=COLOR_PALETTE['error'],
    fc='#FDEDEC',
    lw=1.5
)
error_ax.add_patch(error_box)
error_textbox = TextBox(error_ax, '', initial='Ingrese función y rango [a,b]')
error_textbox.set_active(False)

plt.show()