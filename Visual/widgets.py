import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
from matplotlib.patches import FancyBboxPatch
from Visual.paleta import COLOR_PALETTE

def create_textbox_default(position, text, initial=''):
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
def create_ax_personalized(position,boxstyle,color,fcol,w):
    ax = plt.axes(position)
    ax.axis('off')
    box = FancyBboxPatch(
        (0, 0), 1, 1,
        boxstyle=boxstyle,
        ec=COLOR_PALETTE[color],
        fc=fcol,
        lw=w
    )
    ax.add_patch(box)
    return ax