import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button,TextBox
from matplotlib.patches import FancyBboxPatch
from Visual.paleta import COLOR_PALETTE
from Visual.widgets import create_rounded_widget
from Visual.funcionesNP import add_np_prefix,evaluar_intervalo, return_expo
from Graficar.Updates.left_plots import update_left_plots,update_last_frame
from Graficar.Updates.right_plots import update_right_plots_impl
from Graficar.validarIntegral import es_integral_propia
from scipy.integrate import quad
import warnings

def update_animation(frame):
    n = frame + 1
    if frame == frames - 1:
        update_last_frame(f,a,b)
        global anim
        anim=None
    else:
        update_left_plots(f,a,b,n)
    plt.draw()
def update_right_plots(val):
    n = int(slider.val)
    update_right_plots_impl(f,c,d,n)
def submit(text):
    global f, a, b, c, d, anim, slider, return_button 
    try:
        func_str = add_np_prefix(func_textbox.text)
        a = evaluar_intervalo(interval_a_textbox.text)
        b = evaluar_intervalo(interval_b_textbox.text)
        if b <= a:
            error_textbox.set_val("Error: 'b' debe ser mayor que 'a'")
            return
        if (b - a) > 100:
            error_textbox.set_val("Intervalo máximo: 100 unidades")
            return
        """if (lambda arr: any(arrExp) ):
            if(a<=0):
                return"""
        if return_expo():
            if a < 0 :
                error_textbox.set_val("Error: 'a' debe ser mayor que 0")
                return
        if 'x' not in func_str:
            error_textbox.set_val("La función debe contener 'x'")
            return
        
        try:
            test_x = a + (b - a) * 0.5  
            test_result = eval(func_str, {'np': np, 'x': test_x})
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
                if not es_integral_propia(f, a, b):
                    error_textbox.set_val("Error: Integral impropia (función no definida en el intervalo)")
                    return
                quad(f, a, b)
        except:
            error_textbox.set_val("Función no integrable")
            return
        
        c, d = a, b
        
        for widget in [func_textbox, interval_a_textbox, interval_b_textbox, button,error_textbox]:
            widget.ax.set_visible(False)
        legend_ax.set_visible(False)
        
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

        # Crear botón Regresar
        return_button_ax = plt.axes([0.75, 0.07, 0.15, 0.05])
        return_button_ax.axis('off')
        return_button_box = FancyBboxPatch(
            (0, 0), 1, 1,
            boxstyle="round,pad=0.1,rounding_size=0.1",
            ec=COLOR_PALETTE['primary'],
            fc=COLOR_PALETTE['primary'],
            lw=1.5
        )
        return_button_ax.add_patch(return_button_box)
        return_button = Button(return_button_ax, 'REGRESAR', 
                             color=COLOR_PALETTE['primary'], 
                             hovercolor=COLOR_PALETTE['hover'])
        return_button.label.set_color('white')
        return_button.label.set_fontweight('bold')
        return_button.on_clicked(reset_interface)
        
        update_left_plots(f,a,b,1)
        update_right_plots_impl(f,c,d,1)
        
        plt.draw()
    except ValueError:
        error_textbox.set_val("Valores inválidos")
    except Exception as e:
        error_textbox.set_val(f"Error: {str(e)}")

def reset_interface(event):
    global anim, slider, return_button, fig
    
    # Detener y eliminar la animación
    if anim is not None:
        anim.event_source.stop()
        anim = None
    
    # Eliminar slider y botón de regresar
    if slider is not None:
        slider.ax.remove()
        slider = None
    if return_button is not None:
        return_button.ax.remove()
        return_button = None
    
    # Restaurar elementos iniciales
    for widget in [func_textbox, interval_a_textbox, interval_b_textbox, button, error_textbox]:
        widget.ax.set_visible(True)
    legend_ax.set_visible(True)
    
    # Limpiar todos los axes excepto los widgets
    for ax in fig.axes[:]:
        if ax not in [widget.ax for widget in [func_textbox, interval_a_textbox, interval_b_textbox, button, error_textbox]] + [legend_ax]:
            fig.delaxes(ax)
    
    error_textbox.set_val('Ingrese función e intervalos [a,b] (La máxima longitud entre a,b es 100)')
    plt.draw()

# Configuración inicial
f = lambda x: np.sin(x)
a, b = 0,0
c, d = 0,0
frames = 50

# Crear figura y subplots
fig = plt.figure(figsize=(12, 8), facecolor=COLOR_PALETTE['background'])
plt.subplots_adjust(bottom=0.4)

# Widgets de entrada
func_textbox = create_rounded_widget([0.25, 0.6, 0.5, 0.06], 'f(x) = ', 'sin(x)')
interval_a_textbox = create_rounded_widget([0.25, 0.5, 0.2, 0.06], 'a = ', '0')
interval_b_textbox = create_rounded_widget([0.55, 0.5, 0.2, 0.06], 'b = ', '5')

# Botón con bordes redondeados
button_ax = plt.axes([0.4, 0.4, 0.2, 0.07])
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
error_ax = plt.axes([0.25, 0.3, 0.5, 0.06])
error_ax.axis('off')
error_box = FancyBboxPatch(
    (0, 0), 1, 1,
    boxstyle="round,pad=0.1,rounding_size=0.05",
    ec=COLOR_PALETTE['error'],
    fc='#FDEDEC',
    lw=1.5
)
error_ax.add_patch(error_box)
error_textbox = TextBox(error_ax, '', initial='Ingrese función e intervalos [a,b] (La máxima longitud entre a,b es 100)')
error_textbox.set_active(False)

# Crear leyenda de funciones
legend_text = (
    "Instrucciones:\n"
    "√x → sqrt(x)\n"
    "sen(x) → sin(x)\n"
    "cos(x) → cos(x)\n"
    "tan(x) → tan(x)\n"
    "e^x → exp(x)\n"
    "ln(x) → log(x)\n"
    "x^y → x^y\n"
    "log2(x) → log2(x)\n"
    "log10(x) → log10(x)\n"
    "arcsen(x) → arcsin(x)\n"
    "arccos(x) → arccos(x)\n"
    "arctan(x) → arctan(x)\n"
)

# Configurar posición y estilo de la leyenda
legend_ax = plt.axes([0.85, 0.82, 0.3, 0.15], facecolor='none')
legend_ax.axis('off')

# Crear caja decorativa
legend_box = FancyBboxPatch(
    (0, 0), 1, 1,
    boxstyle="round,pad=0.1,rounding_size=0.05",
    ec=COLOR_PALETTE['secondary'],
    fc=COLOR_PALETTE['background'],
    lw=1
)
legend_ax.add_patch(legend_box)

# Añadir texto
legend_ax.text(
    0.05, 0.95, legend_text,
    ha='left', va='top',
    color=COLOR_PALETTE['text'],
    fontsize=9,
    linespacing=1.5,
    transform=legend_ax.transAxes,
    bbox=dict(
        boxstyle='round,pad=0',
        facecolor='none',
        edgecolor='none'
    )
)
plt.show()