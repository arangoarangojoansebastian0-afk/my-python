import random
import tkinter as tk
from tkinter import messagebox

# --- Configuración de colores base ---
PALETA = {
    "Rojo": (255, 0, 0),
    "Verde": (0, 255, 0),
    "Azul": (0, 0, 255),
    "Cian": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Amarillo": (255, 255, 0),
}

def mezclar(rgb_list, pesos):
    total = sum(pesos)
    if total == 0:
        return (0, 0, 0)
    r = sum(c[0]*w for c, w in zip(rgb_list, pesos)) / total
    g = sum(c[1]*w for c, w in zip(rgb_list, pesos)) / total
    b = sum(c[2]*w for c, w in zip(rgb_list, pesos)) / total
    return (int(round(r)), int(round(g)), int(round(b)))

def rgb_a_hex(rgb):
    return "#%02x%02x%02x" % rgb

class JuegoColores:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Juego de Colores")
        self.root.configure(bg="#1e1e2f")

        self.frame = tk.Frame(root, bg="#1e1e2f", padx=15, pady=15)
        self.frame.pack()

        self.puntos = 0

        # Puntos
        self.lbl_puntos = tk.Label(self.frame, text=f"Puntos: {self.puntos}",
                                   font=("Arial", 14, "bold"), fg="#ffffff", bg="#1e1e2f")
        self.lbl_puntos.grid(row=0, column=0, columnspan=2, pady=(0, 12))

        # Muestras
        self.canvas_obj = tk.Canvas(self.frame, width=200, height=100, bd=3, relief="ridge")
        self.canvas_user = tk.Canvas(self.frame, width=200, height=100, bd=3, relief="ridge")
        self.canvas_obj.grid(row=1, column=0, padx=10, pady=10)
        self.canvas_user.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame, text="Objetivo", font=("Arial", 12, "bold"),
                 fg="#00ffcc", bg="#1e1e2f").grid(row=2, column=0)
        tk.Label(self.frame, text="Tu mezcla", font=("Arial", 12, "bold"),
                 fg="#ffcc00", bg="#1e1e2f").grid(row=2, column=1)

        # Controles
        self.ing_frame = tk.LabelFrame(self.frame, text="Colores disponibles",
                                       font=("Arial", 11, "bold"), fg="white",
                                       bg="#2a2a40", padx=10, pady=10, bd=2)
        self.ing_frame.grid(row=3, column=0, columnspan=2, pady=12)

        # Botones principales
        btns = tk.Frame(self.frame, bg="#1e1e2f")
        btns.grid(row=4, column=0, columnspan=2, pady=(10,0))
        tk.Button(btns, text="Comprobar", command=self.comprobar,
                  bg="#4caf50", fg="white", width=12, font=("Arial", 11, "bold")).grid(row=0, column=0, padx=6)
        tk.Button(btns, text="Reiniciar mezcla", command=self.reiniciar_mezcla,
                  bg="#f44336", fg="white", width=14, font=("Arial", 11, "bold")).grid(row=0, column=1, padx=6)

        # Estado
        self.ingredientes = []
        self.colores_rgb = []
        self.pesos_true = []
        self.pesos_user = []
        self.objetivo = (0,0,0)

        self.nueva_ronda()

    def nueva_ronda(self):
        # Generar objetivo nuevo
        n = random.choice([2,3])
        self.ingredientes = random.sample(list(PALETA.keys()), n)
        self.colores_rgb = [PALETA[nom] for nom in self.ingredientes]
        self.pesos_true = [random.randint(1,3) for _ in range(n)]
        self.objetivo = mezclar(self.colores_rgb, self.pesos_true)
        self.pesos_user = [0]*n

        # UI
        self.dibujar_muestras()
        self.construir_controles_ingredientes()

    def dibujar_muestras(self):
        self.canvas_obj.delete("all")
        self.canvas_user.delete("all")
        self.canvas_obj.create_rectangle(0,0,200,100, fill=rgb_a_hex(self.objetivo), outline="")
        mezcla_user = mezclar(self.colores_rgb, self.pesos_user)
        self.canvas_user.create_rectangle(0,0,200,100, fill=rgb_a_hex(mezcla_user), outline="")

    def construir_controles_ingredientes(self):
        for w in self.ing_frame.winfo_children():
            w.destroy()

        self.contadores = []
        for i, nombre in enumerate(self.ingredientes):
            muestra = tk.Canvas(self.ing_frame, width=40, height=20, bd=1, relief="sunken")
            muestra.create_rectangle(0,0,40,20, fill=rgb_a_hex(PALETA[nombre]), outline="")
            lbl = tk.Label(self.ing_frame, text=nombre, font=("Arial", 11, "bold"),
                           bg="#2a2a40", fg="white")
            cont = tk.Label(self.ing_frame, text="0", width=3,
                            font=("Arial", 11), bg="#2a2a40", fg="#ffcc00")
            self.contadores.append(cont)

            def inc(idx=i):
                if self.pesos_user[idx] < 5:
                    self.pesos_user[idx] += 1
                    self.contadores[idx].config(text=str(self.pesos_user[idx]))
                    self.dibujar_muestras()
            def dec(idx=i):
                if self.pesos_user[idx] > 0:
                    self.pesos_user[idx] -= 1
                    self.contadores[idx].config(text=str(self.pesos_user[idx]))
                    self.dibujar_muestras()

            btn_mas = tk.Button(self.ing_frame, text="+", command=inc,
                                bg="#4caf50", fg="white", width=3)
            btn_menos = tk.Button(self.ing_frame, text="-", command=dec,
                                  bg="#f44336", fg="white", width=3)

            fila = i
            muestra.grid(row=fila, column=0, padx=4, pady=4)
            lbl.grid(row=fila, column=1, padx=6)
            cont.grid(row=fila, column=2, padx=6)
            btn_mas.grid(row=fila, column=3, padx=2)
            btn_menos.grid(row=fila, column=4, padx=2)

    def reiniciar_mezcla(self):
        self.pesos_user = [0]*len(self.pesos_user)
        for cont in self.contadores:
            cont.config(text="0")
        self.dibujar_muestras()

    def dentro_de_tolerancia(self, rgb1, rgb2, tol=6):
        return all(abs(a-b) <= tol for a, b in zip(rgb1, rgb2))

    def comprobar(self):
        mezcla_user = mezclar(self.colores_rgb, self.pesos_user)
        receta = ", ".join(f"{n}: {w}" for n, w in zip(self.ingredientes, self.pesos_true))
        if self.dentro_de_tolerancia(mezcla_user, self.objetivo):
            self.puntos += 1
            messagebox.showinfo("🎉 ¡Correcto!",
                                f"¡Bien hecho! Ganaste +1 punto.\n\nReceta usada:\n{receta}")
        else:
            self.puntos -= 1
            messagebox.showwarning("❌ Fallo",
                                   f"No acertaste, pierdes 1 punto.\n\nLa receta era:\n{receta}")
        self.lbl_puntos.config(text=f"Puntos: {self.puntos}")
        self.nueva_ronda()

if __name__ == "__main__":
    root = tk.Tk()
    JuegoColores(root)
    root.mainloop()
