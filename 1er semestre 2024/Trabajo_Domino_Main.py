class DominoSolver:
    def __init__(self, M, N):
        self.M = M  # Número de filas
        self.N = N  # Número de columnas
        self.board = [[0] * N for _ in range(M)]  # Inicializa el tablero

        # Lista de soluciones (tableros completos)
        self.solutions = []
        
    def initialize_board(self):
        """Inicializa el tablero con todas las casillas vacías."""
        self.board = [[0] * self.N for _ in range(self.M)]

    def is_valid_position(self, row, col, orientation):
        """Verifica si una pieza de dominó puede colocarse en la posición (row, col) con la orientación dada."""
        if orientation == 'H':  # Orientación horizontal
            # Verifica que la pieza se ajuste dentro del tablero y que ambas casillas estén libres
            if col + 1 < self.N and self.board[row][col] == 0 and self.board[row][col + 1] == 0:
                return True
        elif orientation == 'V':  # Orientación vertical
            # Verifica que la pieza se ajuste dentro del tablero y que ambas casillas estén libres
            if row + 1 < self.M and self.board[row][col] == 0 and self.board[row + 1][col] == 0:
                return True
        return False

    def place_domino(self, row, col, orientation):
        """Coloca una pieza de dominó en la posición (row, col) con la orientación dada."""
        if orientation == 'H':  # Orientación horizontal
            self.board[row][col] = 1  # Marca la casilla con 1 para orientación horizontal
            self.board[row][col + 1] = 1
        elif orientation == 'V':  # Orientación vertical
            self.board[row][col] = 2  # Marca la casilla con 2 para orientación vertical
            self.board[row + 1][col] = 2

    def remove_domino(self, row, col, orientation):
        """Elimina una pieza de dominó de la posición (row, col) con la orientación dada."""
        if orientation == 'H':  # Orientación horizontal
            self.board[row][col] = 0  # Restablece las casillas a vacías
            self.board[row][col + 1] = 0
        elif orientation == 'V':  # Orientación vertical
            self.board[row][col] = 0  # Restablece las casillas a vacías
            self.board[row + 1][col] = 0

    def solve(self, row=0, col=0):
        """Función de backtracking para colocar piezas de dominó en el tablero."""
        # Si el tablero está lleno, guardamos la solución
        if row == self.M:
            self.solutions.append([row[:] for row in self.board])
            return
        
        # Si estamos al final de una fila, pasamos a la siguiente
        if col == self.N:
            self.solve(row + 1, 0)
            return
        
        # Si la casilla actual ya está ocupada, pasamos a la siguiente casilla
        if self.board[row][col] != 0:
            self.solve(row, col + 1)
            return
        
        # Intenta colocar una pieza de dominó en orientación horizontal
        if self.is_valid_position(row, col, 'H'):
            self.place_domino(row, col, 'H')
            self.solve(row, col + 2)
            self.remove_domino(row, col, 'H')
        
        # Intenta colocar una pieza de dominó en orientación vertical
        if self.is_valid_position(row, col, 'V'):
            self.place_domino(row, col, 'V')
            self.solve(row, col + 1)
            self.remove_domino(row, col, 'V')
        
    def visualize_board(self):
        """Visualiza el tablero actual."""
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print("\n")

    def print_solutions(self):
        """Imprime todas las soluciones encontradas."""
        print(f"Se encontraron {len(self.solutions)} soluciones:")
        for i, solution in enumerate(self.solutions, start=1):
            print(f"Solución {i}:")
            for row in solution:
                print(' '.join(str(cell) for cell in row))
            print("\n")

def main():
    # Solicitar el tamaño del tablero al usuario
    M = int(input("Ingrese el número de filas (M) del tablero: "))
    N = int(input("Ingrese el número de columnas (N) del tablero: "))

    # Verificar que el tamaño del tablero sea válido (M * N debe ser par)
    if (M * N) % 2 != 0:
        print("El tamaño del tablero (M * N) debe ser par. Por favor, inténtelo de nuevo.")
        return

    # Crear un objeto DominoSolver con las dimensiones del tablero
    solver = DominoSolver(M, N)

    # Encontrar todas las soluciones
    solver.solve()

    # Imprimir todas las soluciones encontradas
    solver.print_solutions()

if __name__ == "__main__":
    main()
