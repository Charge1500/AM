import numpy as np
import matplotlib.pyplot as plt
from Visual.paleta import COLOR_PALETTE
from Graficar.darboaxSum import darboax_sums
from Graficar.graficar import plot_darboax, plot_area_under_curve
from scipy.integrate import quad

def update_left_plots(f,a,b,n):
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
    integral_value, _ = quad(f, a, b)
    
    plt.subplot(2, 2, 1)
    plot_area_under_curve(f, a, b, COLOR_PALETTE['primary'], f'Área Exacta: {integral_value:.4f}')
    
    plt.subplot(2, 2, 3)
    plot_area_under_curve(f, a, b, COLOR_PALETTE['secondary'], f'Área Exacta: {integral_value:.4f}')