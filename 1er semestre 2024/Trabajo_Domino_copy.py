import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import itertools

class DominoSolver:
    def __init__(self, M, N):
        self.M = M
        self.N = N
        self.board = [[0] * N for _ in range(M)]
        self.solutions = []
        
    def initialize_board(self):
        self.board = [[0] * self.N for _ in range(self.M)]
        
    def is_valid_position(self, row, col, orientation):
        if orientation == 'H':
            if col + 1 < self.N and self.board[row][col] == 0 and self.board[row][col + 1] == 0:
                return True
        elif orientation == 'V':
            if row + 1 < self.M and self.board[row][col] == 0 and self.board[row + 1][col] == 0:
                return True
        return False

    def place_domino(self, row, col, orientation):
        if orientation == 'H':
            self.board[row][col] = 1
            self.board[row][col + 1] = 1
        elif orientation == 'V':
            self.board[row][col] = 2
            self.board[row + 1][col] = 2
            
    def remove_domino(self, row, col, orientation):
        if orientation == 'H':
            self.board[row][col] = 0
            self.board[row][col + 1] = 0
        elif orientation == 'V':
            self.board[row][col] = 0
            self.board[row + 1][col] = 0
            
    def solve(self, row=0, col=0):
        if row == self.M:
            # Si se completó el tablero, guarda la solución
            self.solutions.append([row[:] for row in self.board])
            return
        
        # Si col es igual a N, avanzamos a la siguiente fila
        if col == self.N:
            self.solve(row + 1, 0)
            return
        
        # Si la casilla actual está ocupada, avanza a la siguiente casilla
        if self.board[row][col] != 0:
            self.solve(row, col + 1)
            return
        
        # Prueba colocar la pieza de dominó horizontalmente
        if self.is_valid_position(row, col, 'H'):
            self.place_domino(row, col, 'H')
            self.solve(row, col + 2)
            self.remove_domino(row, col, 'H')
        
        # Prueba colocar la pieza de dominó verticalmente
        if self.is_valid_position(row, col, 'V'):
            self.place_domino(row, col, 'V')
            self.solve(row, col + 1)
            self.remove_domino(row, col, 'V')
            
    def get_solutions(self):
        return self.solutions

class DominoVisualizer:
    def __init__(self, solver):
        self.solver = solver
        self.solutions = solver.get_solutions()
        self.current_index = 0
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Soluciones de Dominó")
        plt.subplots_adjust(bottom=0.2)
        
        # Botones para navegar entre las soluciones
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        
        self.btn_prev = Button(axprev, 'Anterior')
        self.btn_prev.on_clicked(self.previous_solution)
        
        self.btn_next = Button(axnext, 'Siguiente')
        self.btn_next.on_clicked(self.next_solution)
        
        # Inicializar visualización con la primera solución
        self.visualize_solution(0)
        
        plt.show()
        
    def visualize_solution(self, solution_index):
        self.ax.clear()
        self.ax.set_xlim(0, self.solver.N)
        self.ax.set_ylim(0, self.solver.M)
        self.ax.set_xticks(range(self.solver.N + 1))
        self.ax.set_yticks(range(self.solver.M + 1))
        self.ax.grid(True)
        
        solution = self.solutions[solution_index]
        
        # Dibuja el tablero con las piezas de dominó
        processed = set()
        for row in range(self.solver.M):
            for col in range(self.solver.N):
                if (row, col) in processed:
                    continue  # Salta a la siguiente casilla si ya ha sido procesada
        
        if solution[row][col] == 1:
            # Pieza de dominó horizontal
            rect = patches.Rectangle((col, self.solver.M - row - 1), 2, 1, edgecolor='black', facecolor='gray', lw=2)
            self.ax.add_patch(rect)
            # Marcar las casillas como procesadas
            processed.add((row, col))
            processed.add((row, col + 1))
        elif solution[row][col] == 2:
            # Pieza de dominó vertical
            rect = patches.Rectangle((col, self.solver.M - row - 1), 1, 2, edgecolor='black', facecolor='gray', lw=2)
            self.ax.add_patch(rect)
            # Marcar las casillas como procesadas
            processed.add((row, col))
            processed.add((row + 1, col))
        
        
        self.fig.canvas.draw()
        
    def next_solution(self, event):
        """Avanza a la siguiente solución."""
        self.current_index = (self.current_index + 1) % len(self.solutions)
        self.visualize_solution(self.current_index)
        
    def previous_solution(self, event):
        """Retrocede a la solución anterior."""
        self.current_index = (self.current_index - 1) % len(self.solutions)
        self.visualize_solution(self.current_index)

def main():
    # Solicitar al usuario el tamaño del tablero
    M = int(input("Ingrese el número de filas (M) del tablero: "))
    N = int(input("Ingrese el número de columnas (N) del tablero: "))
    
    # Verificar que el producto M * N sea par
    if M * N % 2 != 0:
        print("El producto de M y N debe ser par para que haya una solución.")
        return
    
    # Crear un objeto de DominoSolver
    solver = DominoSolver(M, N)
    
    # Resolver el problema
    solver.solve()
    
    # Verificar si se encontraron soluciones
    if not solver.get_solutions():
        print("No se encontraron soluciones.")
        return
    
    # Crear un objeto de DominoVisualizer
    DominoVisualizer(solver)

if __name__ == "__main__":
    main()
