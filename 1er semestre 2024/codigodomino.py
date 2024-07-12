def is_valid(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == 0

def can_place(board, row, col):
    return is_valid(board, row, col) and is_valid(board, row + 1, col)

def place_domino(board, row, col):
    board[row][col] = 1
    board[row + 1][col] = 1

def remove_domino(board, row, col):
    board[row][col] = 0
    board[row + 1][col] = 0

def print_board(board):
    for row in board:
        print(row)

def solve_domino(board, row, col):
    if row == len(board):
        print_board(board)
        print()
        return

    next_row = row + (col + 1) // len(board[0])
    next_col = (col + 1) % len(board[0])

    if can_place(board, row, col):
        place_domino(board, row, col)
        solve_domino(board, next_row, next_col)
        remove_domino(board, row, col)

    solve_domino(board, next_row, next_col)

def main():
    M = int(input("Ingrese el número de filas (M): "))
    N = int(input("Ingrese el número de columnas (N): "))

    if M * N % 2 != 0:
        print("No hay solución para un tablero de tamaño impar.")
        return

    board = [[0 for _ in range(N)] for _ in range(M)]
    solve_domino(board, 0, 0)

if __name__ == "__main__":
    main()