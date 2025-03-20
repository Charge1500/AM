import numpy as np
import matplotlib.pyplot as plt
from Visual.paleta import COLOR_PALETTE
from Graficar.darboaxSum import darboax_sums
from Graficar.graficar import plot_darboax

def update_right_plots_impl(f,c,d,n):
    for i in [2, 4]:
        plt.subplot(2, 2, i)
        plt.cla()
    
    lower_sum_sub, upper_sum_sub, x_sub = darboax_sums(f, c, d, n)
    
    plt.subplot(2, 2, 2)
    plot_darboax(f, c, d, n, x_sub, lower_sum_sub, COLOR_PALETTE['primary'], 'Suma Inferior (Subintervalo)')
    
    plt.subplot(2, 2, 4)
    plot_darboax(f, c, d, n, x_sub, upper_sum_sub, COLOR_PALETTE['secondary'], 'Suma Superior (Subintervalo)')
    
    plt.draw()