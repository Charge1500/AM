import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button,TextBox
from matplotlib.patches import FancyBboxPatch
from Visual.paleta import COLOR_PALETTE
from Visual.widgets import create_rounded_widget
from Visual.funcionesNP import add_np_prefix
from Graficar.Updates.left_plots import update_left_plots,update_last_frame
from Graficar.Updates.right_plots import update_right_plots_impl
from scipy.integrate import quad
import warnings

def update_animation(frame):
    n = frame + 1
    if frame == frames - 1:
        update_last_frame(f,a,b)
    else:
        update_left_plots(f,a,b,n)
    plt.draw()
def update_right_plots(val):
    n = int(slider.val)
    update_right_plots_impl(f,c,d,n)

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
        
        for widget in [func_textbox, interval_a_textbox, interval_b_textbox, button,error_textbox]:
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
        update_left_plots(f,a,b,1)
        update_right_plots_impl(f,c,d,1)
        
        plt.draw()
    except ValueError:
        error_textbox.set_val("Valores inválidos")
    except Exception as e:
        error_textbox.set_val(f"Error: {str(e)}")

# Configuración inicial
f = lambda x: np.sin(x)
a, b = 0,0
c, d = 0,0
frames = 50

# Crear figura
fig = plt.figure(figsize=(12, 8), facecolor=COLOR_PALETTE['background'])
plt.subplots_adjust(bottom=0.4)

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
error_textbox = TextBox(error_ax, '', initial='Ingrese función e intervalos [a,b] (La máxima longitud entre a,b solo puede ser 25)')
error_textbox.set_active(False)

plt.show()