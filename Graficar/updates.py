import numpy as np
import matplotlib.pyplot as plt
from Visual.paleta import COLOR_PALETTE
from Graficar.graficar import plot_darboux, plot_area_under_curve,darboux_sums
from scipy.integrate import quad

def update_left_plots(f,a,b,n):
    for i in [1, 3]:
        plt.subplot(2, 2, i)
        plt.cla()
    
    lower_sum_main, upper_sum_main, x_main = darboux_sums(f, a, b, n)
    
    plt.subplot(2, 2, 1)
    plot_darboux(f, a, b, n, x_main, lower_sum_main, COLOR_PALETTE['primary'], 'Suma Inferior')
    
    plt.subplot(2, 2, 3)
    plot_darboux(f, a, b, n, x_main, upper_sum_main, COLOR_PALETTE['secondary'], 'Suma Superior')

def update_last_frame(f,a,b):
    for i in [1, 3]:
        plt.subplot(2, 2, i)
        plt.cla()
    
    integral_value, _ = quad(f, a, b)
    integral_value, _ = quad(f, a, b)
    
    plt.subplot(2, 2, 1)
    plot_area_under_curve(f, a, b, COLOR_PALETTE['primary'], f'Área Exacta: {integral_value:.4f}')
    
    plt.subplot(2, 2, 3)
    plot_area_under_curve(f, a, b, COLOR_PALETTE['secondary'], f'Área Exacta: {integral_value:.4f}')

def update_right_plots_impl(f,c,d,n):
    for i in [2, 4]:
        plt.subplot(2, 2, i)
        plt.cla()
    
    lower_sum_sub, upper_sum_sub, x_sub = darboux_sums(f, c, d, n)
    
    plt.subplot(2, 2, 2)
    plot_darboux(f, c, d, n, x_sub, lower_sum_sub, COLOR_PALETTE['primary'], 'Suma Inferior (Subintervalo)')
    
    plt.subplot(2, 2, 4)
    plot_darboux(f, c, d, n, x_sub, upper_sum_sub, COLOR_PALETTE['secondary'], 'Suma Superior (Subintervalo)')
    
    plt.draw()