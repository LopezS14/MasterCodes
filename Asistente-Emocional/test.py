# ==========================================
# Diagrama MLP: "Clasificación totalmente conectada"
# Autor: Alfredo HM — Estilo igual al diagrama CNN
# ==========================================

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D

# --- Configuración general ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Computer Modern Roman', 'CMU Serif', 'DejaVu Serif', 'Times New Roman']
plt.rcParams['font.weight'] = 'bold'

# Colores
BLUE = "#1f4aa5"
EDGE = BLUE
LINE = "#86a6e5"

# --- Parámetros del diagrama ---
fig, ax = plt.subplots(figsize=(19, 6))
ax.set_facecolor('none')
fig.patch.set_alpha(0.0)
ax.axis("off")

y_base = 0
by = y_base - 0.5
h = 1.2

# --- Capa de entrada ---
x = 0.8
ax.text(x, by + h + 0.6, "Características de entrada", fontsize=16, fontweight="bold", ha="center")
for i in range(8):
    cy = by + 1.1 - i*0.3
    ax.add_patch(Circle((x, cy), 0.09, ec=EDGE, fc="#ffffff", lw=1.8))

# --- Capa densa 128 ---
x_dense1 = x + 2.2
ax.text(x_dense1, by + h + 0.6, "Capa densa\n128 neuronas, ReLU", fontsize=15, fontweight="bold", ha="center")
for i in range(10):
    cy = by + 1.3 - i*0.26
    ax.add_patch(Circle((x_dense1, cy), 0.09, ec=EDGE, fc="#ffffff", lw=1.8))
# Flechas de conexión
for i in range(8):
    for j in range(10):
        ax.plot([x+0.09, x_dense1-0.09], [by+1.1 - i*0.3, by+1.3 - j*0.26],
                linestyle=":", linewidth=1, color=LINE)

# --- Dropout 0.5 ---
x_drop1 = x_dense1 + 1.2
ax.add_patch(Rectangle((x_drop1 - 0.05, by - 0.3), 0.1, 2.4, color="#000000", alpha=0.15))
ax.text(x_drop1 + 0.4, by + h + 0.6, "Dropout 0.5", fontsize=14, fontweight="bold", ha="center", color="#333333")

# --- Capa densa 64 ---
x_dense2 = x_drop1 + 1.6
ax.text(x_dense2, by + h + 0.6, "Capa densa\n64 neuronas, ReLU", fontsize=15, fontweight="bold", ha="center")
for i in range(8):
    cy = by + 1.1 - i*0.3
    ax.add_patch(Circle((x_dense2, cy), 0.09, ec=EDGE, fc="#ffffff", lw=1.8))
for i in range(10):
    for j in range(8):
        ax.plot([x_dense1+0.09, x_dense2-0.09],
                [by+1.3 - i*0.26, by+1.1 - j*0.3],
                linestyle=":", linewidth=1, color=LINE)

# --- Dropout 0.7 ---
x_drop2 = x_dense2 + 1.2
ax.add_patch(Rectangle((x_drop2 - 0.05, by - 0.3), 0.1, 2.4, color="#000000", alpha=0.15))
ax.text(x_drop2 + 0.4, by + h + 0.6, "Dropout 0.7", fontsize=14, fontweight="bold", ha="center", color="#333333")

# --- Capa de salida ---
x_out = x_drop2 + 1.8
ax.text(x_out, by + h + 0.6, "Capa de salida\nSoftmax\n(Clases de salida)", fontsize=15, fontweight="bold", ha="center")
for i in range(4):
    cy = by + 0.9 - i*0.4
    ax.add_patch(Circle((x_out, cy), 0.09, ec=EDGE, fc="#ffffff", lw=1.8))
for i in range(8):
    for j in range(4):
        ax.plot([x_dense2+0.09, x_out-0.09],
                [by+1.1 - i*0.3, by+0.9 - j*0.4],
                linestyle=":", linewidth=1, color=LINE)

# --- Llave negra superior ---
def draw_down_bracket(ax, x_left, x_right, y_top, drop=0.55, tilt=-0.05, color="#000000", lw=3.2):
    ax.add_line(Line2D([x_left, x_left], [y_top, y_top - drop], lw=lw, color=color))
    ax.add_line(Line2D([x_left, x_right], [y_top - drop, y_top - drop + tilt*(x_right-x_left)], lw=lw, color=color))
    ax.add_line(Line2D([x_right, x_right], [y_top - drop + tilt*(x_right-x_left), y_top], lw=lw, color=color))

br_y = by + h + 1.5
draw_down_bracket(ax, x_dense1 - 0.6, x_out + 0.5, br_y, drop=0.6, tilt=-0.05)
ax.text((x_dense1 + x_out)/2, br_y + 0.4, "Clasificación totalmente conectada",
        fontsize=16, fontweight="bold", ha="center", color="#000000")

# --- Guardar ---
plt.savefig("mlp_diagrama_final.png", dpi=300, bbox_inches="tight", transparent=True)
plt.show()
print("✅ Diagrama guardado como mlp_diagrama_final.png")
