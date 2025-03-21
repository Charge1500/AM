import matplotlib.pyplot as plt

COLOR_PALETTE = {
    'background': '#F5F5F5',
    'primary': '#4A90E2',
    'secondary': '#2C3E50',
    'error': '#E74C3C',
    'text': '#2C3E50',
    'widget': '#4A90E2',
    'hover': '#357ABD'
}

plt.style.use('seaborn-v0_8-darkgrid')

legend_text = (
    "Instrucciones:\n"
    "√x → sqrt(x)\n"
    "sen(x) → sin(x)\n"
    "cos(x) → cos(x)\n"
    "tan(x) → tan(x)\n"
    "ln(x) → log(x)\n"
    "x^y → pow(x, y)\n"
    "log2(x) → log2(x)\n"
    "log10(x) → log10(x)\n"
    "arcsen(x) → arcsin(x)\n"
    "arccos(x) → arccos(x)\n"
    "arctan(x) → arctan(x)\n"
)