import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox
from scipy.integrate import quad
import warnings

# Función para calcular las sumas de Darboax inferiores y superiores
def darboax_sums(f, a, b, n):  
    x = np.linspace(a, b, n + 1)
    dx = (b - a) / n  
    lower_sum = 0
    upper_sum = 0
    for i in range(n):
        x_left = x[i] 
        x_right = x[i + 1] 
        # Ínfimo y supremo en el subintervalo [x_left, x_right]
        m_i = min(f(np.linspace(x_left, x_right, 100))) 
        M_i = max(f(np.linspace(x_left, x_right, 100))) 
        lower_sum += m_i * dx #Suma el área del rectángulo inferior (altura m_i,ancho dx) a la suma inferior
        upper_sum += M_i * dx #Suma el área del rectángulo superior (altura M_i,ancho dx) a la suma superior
    return lower_sum, upper_sum, x

# Función para actualizar la animación (gráficos de la izquierda)
def update_animation(frame):
    n = frame + 1  # Número de subintervalos
    if(frame == frames - 1):
        update_last_frame()
    else:
        update_left_plots(n) # Actualizar gráficos de la izquierda
    
    plt.draw() #Actualiza la figura en la ventana gráfica para ver los cambios realizados en los gráficos

# Función para actualizar los gráficos de la izquierda
def update_left_plots(n):
    # Limpiar solo los subgráficos de la izquierda
    for i in [1, 3]:  # Subgráficos 1 y 3 
        plt.subplot(2, 2, i) #Selecciona el subgráfico correspondiente
        plt.cla()  # Limpiar el subgráfico actual
    
    # Intervalo completo [a, b]
    lower_sum_main, upper_sum_main, x_main = darboax_sums(f, a, b, n)
    
    # Sumas inferiores
    plt.subplot(2, 2, 1)  # Fila 1, Columna 1
    plot_darboax(f, a, b, n, x_main, lower_sum_main, 'green', 'Suma Inferior (Intervalo Completo)') 
    # Sumas superiores
    plt.subplot(2, 2, 3)  # Fila 2, Columna 1
    plot_darboax(f, a, b, n, x_main, upper_sum_main, 'red', 'Suma Superior (Intervalo Completo)')

# Función para actualizar el último frame
def update_last_frame():
    # Limpiar solo los subgráficos de la izquierda
    for i in [1, 3]:  # Subgráficos 1 y 3
        plt.subplot(2, 2, i)
        plt.cla()  # Limpiar el subgráfico actual
    
    # Calcular el valor exacto de la integral
    integral_value, _ = quad(f, a, b)  # Calcula la integral definida de f en [a, b]
    
    # Área bajo la curva (sin rectángulos)
    plt.subplot(2, 2, 1)  # Fila 1, Columna 1
    plot_area_under_curve(f, a, b, 'green', f'Área bajo la curva (Suma Inferior = {integral_value:.4f})')
    
    plt.subplot(2, 2, 3)  # Fila 2, Columna 1
    plot_area_under_curve(f, a, b, 'red', f'Área bajo la curva (Suma Superior = {integral_value:.4f})')

# Función para graficar el área bajo la curva
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

# Función para actualizar los gráficos de la derecha (con el slider)
def update_right_plots(val):
    n = int(slider.val)  # Número de subintervalos (valor del slider)
    update_right_plots_impl(n)

# Función auxiliar para actualizar los gráficos de la derecha
def update_right_plots_impl(n):
    # Limpiar solo los subgráficos de la derecha
    for i in [2, 4]:  # Subgráficos 2 y 4
        plt.subplot(2, 2, i) #Selecciona el subgráfico correspondiente
        plt.cla()  # Limpiar el subgráfico actual
    
    # Subintervalo [c, d]
    lower_sum_sub, upper_sum_sub, x_sub = darboax_sums(f, c, d, n)
    
    # Sumas inferiores
    plt.subplot(2, 2, 2)  # Fila 1, Columna 2
    plot_darboax(f, c, d, n, x_sub, lower_sum_sub, 'green', 'Suma Inferior (Subintervalo)')
    
    # Sumas superiores
    plt.subplot(2, 2, 4)  # Fila 2, Columna 2
    plot_darboax(f, c, d, n, x_sub, upper_sum_sub, 'red', 'Suma Superior (Subintervalo)')
    
    plt.draw()

# Función auxiliar para graficar sumas de Darboax
def plot_darboax(f, a, b, n, x_partition, sum_value, color, title):
    x_vals = np.linspace(a, b, 1000)
    y_vals = f(x_vals)

    plt.plot(x_vals, y_vals, 'b-', label='Función $f(x)$')

    # Tipo de suma (inferior o superior)
    is_lower = color == 'green' #si es verde sumas inferiores y en caso contrario será rojo(sumas superiores)
    
    for i in range(len(x_partition) - 1):
        x_left = x_partition[i]
        x_right = x_partition[i + 1]
        # Calcular m_i o M_i
        values = f(np.linspace(x_left, x_right, 100))
        height = min(values) if is_lower else max(values)
        
        plt.fill_between([x_left, x_right], [0, 0], [height, height], #Dibuja un rectángulo entre [x_left, x_right] y [0, height]
                        color=color, alpha=0.5, #Color del rectángulo y transparencia
                        label='Suma Inferior' if (i == 0 and is_lower) else #Etiqueta para la leyenda del gráfico.Solo se añade en el primer subintervalo para q no se duplique
                              'Suma Superior' if (i == 0 and not is_lower) else "")

    plt.title(f'{title} (n = {n})\nSuma = {sum_value:.4f}')
    plt.xlabel('x') #Etiquetas del eje 'x' y 'y'
    plt.ylabel('y')
    plt.legend() #Muestra la leyenda del gráfico.
    plt.grid() #Añade una cuadrícula al gráfico.

# Función para agregar automáticamente 'np.' a las funciones matemáticas
def add_np_prefix(func_str):
    # Lista de funciones matemáticas comunes
    math_functions = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'arcsin', 'arccos', 'arctan']
    for func in math_functions:
        func_str = func_str.replace(f"{func}(", f"np.{func}(")
    return func_str

# Función para manejar el evento del botón "Aceptar"
def submit(text):
    global f, a, b, c, d
    try:
        # Obtener la función y los intervalos de los cuadros de texto
        func_str = func_textbox.text
        a = float(interval_a_textbox.text)
        b = float(interval_b_textbox.text)
        
        # Validar el intervalo
        if b <= a:
            error_textbox.set_val("Error: 'b' debe ser mayor que 'a'.")
            return
        if (b - a) > 25:
            error_textbox.set_val("Error: El intervalo (b - a) debe ser <= 25.")
            return
        
        # Validar que la función esté evaluada en x
        if 'x' not in func_str:
            error_textbox.set_val("Error: La función debe estar evaluada en 'x'.")
            return
        
        # Agregar automáticamente 'np.' a las funciones matemáticas
        func_str = add_np_prefix(func_str)
        
        # Validar la función
        try:
            # Probar la función con un valor de prueba
            test_x = 1.0
            test_result = eval(func_str, {'np': np, 'x': test_x})
            if not isinstance(test_result, (int, float)):
                error_textbox.set_val("Error: Función no válida.")
                return
        except Exception as e:
            error_textbox.set_val("Error: Función no válida.")
            return
        
        # Definir la función
        f = lambda x: eval(func_str, {'np': np, 'x': x})
        
        # Verificar si la función es integrable en el intervalo [a, b]
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("error")  # Convertir advertencias en excepciones
                integral_value, _ = quad(f, a, b)
        except Exception as e:
            error_textbox.set_val("Error: La función no es integrable en el intervalo dado.")
            return
        
        # Configurar el subintervalo [c, d] igual al intervalo completo [a, b]
        c, d = a, b
        
        # Eliminar los cuadros de texto y el botón
        func_textbox.ax.set_visible(False)
        interval_a_textbox.ax.set_visible(False)
        interval_b_textbox.ax.set_visible(False)
        button.ax.set_visible(False)
        error_textbox.ax.set_visible(False)
        
        # Ajustar el espacio para los gráficos
        plt.subplots_adjust(bottom=0.1, hspace=0.5)
        
        # Iniciar la animación
        global anim
        anim = FuncAnimation(fig, update_animation, frames=frames, interval=500, repeat=False)
        
        # Añadir slider
        ax_slider = plt.axes([0.6, 0.025, 0.3, 0.03])
        global slider
        slider = Slider(ax_slider, 'Intervalos (n)', 1, 300, valinit=1, valstep=1)
        slider.on_changed(update_right_plots)
        
        # Dibujar gráficos iniciales
        update_left_plots(1)
        update_right_plots_impl(1)
        
        plt.draw()
    except ValueError:
        error_textbox.set_val("Error: 'a' y 'b' deben ser números válidos.")
    except Exception as e:
        error_textbox.set_val(f"Error: {e}")

# Configuración inicial
f = lambda x: np.sin(x)  # Función por defecto
a, b = 0, np.pi         # Intervalo por defecto
c, d = 0, np.pi
frames = 51

# Crear la figura y los cuadros de texto
fig = plt.figure(figsize=(12, 8))
plt.subplots_adjust(bottom=0.4)

# Cuadro de texto para la función
ax_func = plt.axes([0.3, 0.6, 0.4, 0.05])
func_textbox = TextBox(ax_func, 'f(x)', initial='sin(x)')

# Cuadro de texto para el intervalo a
ax_interval_a = plt.axes([0.3, 0.5, 0.18, 0.05])
interval_a_textbox = TextBox(ax_interval_a, 'a', initial='0')

# Cuadro de texto para el intervalo b
ax_interval_b = plt.axes([0.52, 0.5, 0.18, 0.05])
interval_b_textbox = TextBox(ax_interval_b, 'b', initial='5')

# Cuadro de texto para mostrar errores (no editable)
ax_error = plt.axes([0.3, 0.4, 0.4, 0.05])
error_textbox = TextBox(ax_error, 'Mensajes de error', initial='Buen día camarada')
error_textbox.set_active(False)  # Deshabilitar la edición

# Botón "Aceptar"
ax_button = plt.axes([0.4, 0.3, 0.2, 0.075])
button = Button(ax_button, 'Aceptar')
button.on_clicked(submit)

plt.show()