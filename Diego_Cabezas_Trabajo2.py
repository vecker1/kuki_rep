from contextlib import nullcontext
import tkinter as tk
from tkinter import font
import random
#Librerias a ocupar

class Tableroajedrez:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabajo 2 GRAFOS - Diego Cabezas")
        self.tablero = [[None for _ in range(8)] for _ in range(8)]
        self.fila_actual = -1
        self.columna_actual = 0
        self.crear_tablero()
        self.crear_controles()
        self.aumentar_fuente()
#clase para creacion,interfaz,gestion,movimiento,y gui

    def crear_tablero(self): #funcion encargada de crear el tablero con la libreria tkinter
        for fila in range(8):
            for columna in range(8):
                color = "white" if (fila + columna) % 2 == 0 else "grey"
                celda = tk.Label(self.root, text="",bd=1.5, relief="solid", width=9, height=4, bg=color)
                celda.grid(row=fila, column=columna)
                self.tablero[fila][columna] = celda

        for i, letras in enumerate("ABCDEFGH"):
            tk.Label(self.root, text=letras, width=11, height=4, bd=1.5, relief="solid", bg="lightgrey").grid(row=8, column=i) #FILA
            tk.Label(self.root, text=str(8 - i), width=10, height=4,bd=1.5, relief="solid", bg="lightgrey").grid(row=i, column=8) #COLUMNA

    def crear_controles(self): #crear botones con tkinter y sus funciones
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=9, columnspan=8)

        tk.Label(control_frame, text="Posición inicial (Ejemplo: G4):").pack(side=tk.LEFT)
        self.entry = tk.Entry(control_frame)
        self.entry.pack(side=tk.LEFT)
        tk.Button(control_frame, text="Iniciar\nRecorrido", command=self.iniciar_caballo).pack(side=tk.LEFT)

        tk.Button(control_frame, text="Reiniciar\n(Solo cuando finalice)", command=self.reniciar_caballo).pack(side=tk.LEFT)

    def reniciar_caballo(self): #renicia y limpia la posicion del caballo
        self.reniciar_tablero()
        self.root.update()

    def reniciar_tablero(self): #limpia los datos en pantalla
        for fila in range(8):
            for columna in range(8):
                self.tablero[fila][columna].config(text="")
        self.fila_actual = -1
        self.columna_actual = 0

    def mover_caballo(self, nueva_fila, nueva_columna, cont_movimientos): #movimientos del caballo
    
        self.tablero[self.fila_actual][self.columna_actual].config(text=cont_movimientos)

        self.fila_actual = nueva_fila
        self.columna_actual = nueva_columna

        self.tablero[nueva_fila][nueva_columna].config(text="♞")

    def iniciar_caballo(self): #crea las etiquetas y guarda la posicion ingresada
        posicion_inicial = self.entry.get().upper()  
        if len(posicion_inicial) == 2 and posicion_inicial[0] in "ABCDEFGH" and posicion_inicial[1] in "12345678":
            columna = ord(posicion_inicial[0]) - ord('A')
            fila = 7 - (int(posicion_inicial[1]) - 1)
            self.mover_caballo(fila, columna, None)  
            self.movimiento_caballo(fila, columna, 1) 
        else:
            print("Posición inicial no válida. Utiliza el formato 'A1', 'B2', etc.")

    def movimiento_caballo(self, fila, columna, cont_movimientos): #lista de movimiento del caballo
        movimientos = [(-2, -1), (-2, 1),(-1, -2), (-1, 2),(1, -2), (1, 2),(2, -1), (2, 1)]
        movimientos_disponibles = []

        for fd, cd in movimientos:  #"fd" (fila de desplazamiento) || "dr" (columna de desplazamiento).
            nueva_fila, nueva_columna = fila + fd, columna + cd
            if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8 and self.tablero[nueva_fila][nueva_columna].cget('text') == "":
                neighbor_moves = self.func_calculo(nueva_fila, nueva_columna)
                movimientos_disponibles.append((len(neighbor_moves), nueva_fila, nueva_columna))

        if movimientos_disponibles:
            movimientos_disponibles.sort()
            _, siguiente_fila, siguiente_columna = movimientos_disponibles[0]
            self.mover_caballo(siguiente_fila, siguiente_columna, cont_movimientos)
            self.root.update()
            self.root.after(500) 
            self.movimiento_caballo(siguiente_fila, siguiente_columna, cont_movimientos + 1)
        else:
            print("Recorrido completo.")

    def func_calculo(self, fila, columna): #calcular solucion
        movimientos = [(-2, -1), (-2, 1),(-1, -2), (-1, 2),(1, -2), (1, 2),(2, -1), (2, 1)]
        movimientos_cercanos = []
        for fd, cd in movimientos:  #"fd" (fila de desplazamiento) || "dr" (columna de desplazamiento).
            nueva_fila, nueva_columna = fila + fd, columna + cd
            if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8 and self.tablero[nueva_fila][nueva_columna].cget('text') == "":
                movimientos_cercanos.append((nueva_fila, nueva_columna))
        return movimientos_cercanos
    
    def aumentar_fuente(self):
        fuente_personalizada = font.Font(family="Helvetica", size=12) 
        for fila in range(8):
            for columna in range(8):
                self.tablero[fila][columna]['font'] = fuente_personalizada
        self.entry['font'] = fuente_personalizada
        self.entry['width'] = 10 
        self.root.update()


if __name__ == "__main__":
    root = tk.Tk()
    tablero = Tableroajedrez(root)
    root.mainloop()
