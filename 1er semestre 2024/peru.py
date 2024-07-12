import pygame
from typing import List, Set

class DominoBoard:
    def _init_(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.board = [[0] * cols for _ in range(rows)]
        self.solutions: List[List[List[int]]] = []
        self.found_solutions: Set[str] = set()

    def is_valid_board(self) -> bool:
        return self.rows * self.cols % 2 == 0

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def can_place_domino(self, row: int, col: int, direction: str) -> bool:
        if direction == "horizontal":
            return (self.is_valid_position(row, col + 1) and
                    self.board[row][col] == 0 and
                    self.board[row][col + 1] == 0)
        elif direction == "vertical":
            return (self.is_valid_position(row + 1, col) and
                    self.board[row][col] == 0 and
                    self.board[row + 1][col] == 0)
        return False

    def place_domino(self, row: int, col: int, direction: str) -> None:
        if direction == "horizontal":
            self.board[row][col] = 1
            self.board[row][col + 1] = 1
        elif direction == "vertical":
            self.board[row][col] = 2
            self.board[row + 1][col] = 2

    def is_solution(self) -> bool:
        return all(cell != 0 for row in self.board for cell in row)

    def has_row_conflict(self, row: int, col: int, direction: str) -> bool:
        if direction == "horizontal":
            return not (2 in self.board[row] or 0 in self.board[row])
        elif direction == "vertical":
            for r in range(row, self.rows - 1):
                if self.board[r][col] == self.board[r + 1][col] == 0:
                    return False
        return True

    def has_column_conflict(self, row: int, col: int, direction: str) -> bool:
        if direction == "vertical":
            return all(self.board[r][col] != 1 for r in range(self.rows))
        elif direction == "horizontal":
            for r in range(row, self.rows - 1):
                if self.board[r][col] == self.board[r + 1][col] == 0:
                    return False
        return True

    def contains_value(self, array: List[int], value: int) -> bool:
        return value in array

    def find_solutions(self, row: int, col: int) -> None:
        if self.is_solution():
            solution = [row[:] for row in self.board]
            solution_string = self.array_to_string(solution)
            if solution_string not in self.found_solutions:
                self.found_solutions.add(solution_string)
                self.solutions.append(solution)
            return

        for r in range(row, self.rows):
            for c in range(col if r == row else 0, self.cols):
                if self.board[r][c] == 0:
                    if self.can_place_domino(r, c, "horizontal"):
                        self.place_domino(r, c, "horizontal")
                        if (self.has_row_conflict(r, c, "horizontal") and
                                self.has_column_conflict(r, c, "horizontal")):
                            self.find_solutions(r, c + 2 if c + 2 < self.cols else r + 1)
                        self.remove_domino(r, c, "horizontal")
                    if self.can_place_domino(r, c, "vertical"):
                        self.place_domino(r, c, "vertical")
                        if (self.has_row_conflict(r, c, "vertical") and
                                self.has_column_conflict(r, c, "vertical")):
                            self.find_solutions(r, c + 1 if c + 1 < self.cols else r + 1)
                        self.remove_domino(r, c, "vertical")

    def remove_domino(self, row: int, col: int, direction: str) -> None:
        if direction == "horizontal":
            self.board[row][col] = 0
            self.board[row][col + 1] = 0
        elif direction == "vertical":
            self.board[row][col] = 0
            self.board[row + 1][col] = 0

    def print_all_solutions(self) -> None:
        print("Total solutions:", len(self.solutions))
        for i, solution in enumerate(self.solutions):
            print("Solution", i + 1, ":")
            for row in solution:
                print(' '.join(map(str, row)))
            print()

    def array_to_string(self, array: List[List[int]]) -> str:
        return ''.join(map(str, [cell for row in array for cell in row]))

    def draw_board(self, screen: pygame.Surface) -> None:
        cell_size = 40
        gap = 10
        margin_x = 50
        margin_y = 50

        for row in range(self.rows):
            for col in range(self.cols):
                color = (255, 255, 255) if self.board[row][col] == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (margin_x + col * (cell_size + gap),margin_y + row * (cell_size + gap),cell_size, cell_size))
                if self.board[row][col] == 1:
                    pygame.draw.rect(screen, (255, 0, 0), (margin_x + col * (cell_size + gap),margin_y + row * (cell_size + gap), cell_size, cell_size))
                elif self.board[row][col] == 2:
                    pygame.draw.rect(screen, (0, 0, 255), (margin_x + col * (cell_size + gap),margin_y + row * (cell_size + gap),cell_size, cell_size))

    def draw_solutions(self, screen: pygame.Surface) -> None:
        margin_x = 50
        margin_y = 50 + self.rows * 50 + 20

        for i, solution in enumerate(self.solutions):
            pygame.draw.rect(screen, (200, 200, 200), (margin_x, margin_y + i * 50,
                                                       self.cols * 50, 40))
            font = pygame.font.Font(None, 36)
            text = font.render(f"Solution {i + 1}", True, (0, 0, 0))
            screen.blit(text, (margin_x + 10, margin_y + i * 50))

            for row in range(self.rows):
                for col in range(self.cols):
                    color = (255, 255, 255) if solution[row][col] == 0 else (0, 0, 0)
                    pygame.draw.rect(screen, color, (margin_x + col * 50, margin_y + i * 50 + row * 50, 40, 40))
                    if solution[row][col] == 1:
                        pygame.draw.rect(screen, (255, 0, 0), (margin_x + col * 50, margin_y + i * 50 + row * 50,40, 40))
                    elif solution[row][col] == 2:
                        pygame.draw.rect(screen, (0, 0, 255), (margin_x + col * 50, margin_y + i * 50 + row * 50,40, 40))

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((255, 255, 255))
        self.draw_board(screen)
        self.draw_solutions(screen)

        pygame.display.flip()

if __name__ == "_main_":
    rows = int(input("Ingrese el número de filas: "))
    cols = int(input("Ingrese el número de columnas: "))

    domino_board = DominoBoard(rows, cols)
    if domino_board.is_valid_board():
        domino_board.find_solutions(0, 0)

        pygame.init()
        screen = pygame.display.set_mode((cols * 50 + 100, rows * 50 + len(domino_board.solutions) * 50 + 200))
        pygame.display.set_caption("Dominó Solver")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            domino_board.draw(screen)

        pygame.quit()
    else:
        print("Tablero no válido")
