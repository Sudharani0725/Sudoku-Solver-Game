import tkinter as tk
from tkinter import messagebox
import time, random

root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("600x650")
root.configure(bg="white")

entries = [[None for _ in range(9)] for _ in range(9)]

# Function to determine background color (optional)
def get_bg_color(i, j):
    return "#ffffff"  # keep white like reference puzzle

# Build the Sudoku grid with bold 3x3 subgrid borders
block_frames = [[None for _ in range(3)] for _ in range(3)]

for bi in range(3):      # block row
    for bj in range(3):  # block col
        block = tk.Frame(root, bd=3, relief="solid")  # thick black border
        block.grid(row=bi, column=bj, padx=2, pady=2)
        block_frames[bi][bj] = block

        # place 3x3 entries inside each block
        for i in range(3):
            for j in range(3):
                gi, gj = 3*bi + i, 3*bj + j  # global i, j
                e = tk.Entry(block, width=2, font=('Arial', 18), justify='center',
                             bd=1, relief="solid", bg=get_bg_color(gi, gj))
                e.grid(row=i, column=j, padx=1, pady=1)
                entries[gi][gj] = e

# Extract the grid from user input
def get_grid():
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            val = entries[i][j].get()
            if val == '':
                row.append(0)
            elif val.isdigit() and 1 <= int(val) <= 9:
                row.append(int(val))
            else:
                entries[i][j].config(bg='salmon')
                messagebox.showerror("Invalid Input", f"Invalid entry at row {i+1}, column {j+1}")
                return None
        grid.append(row)
    return grid

# Check if placing a number is valid
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row//3), 3 * (col//3)
    for i in range(start_row, start_row+3):
        for j in range(start_col, start_col+3):
            if board[i][j] == num:
                return False
    return True

# Recursive backtracking solver
def solve_board(board, step_by_step=False):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if step_by_step:
                            entries[i][j].delete(0, tk.END)
                            entries[i][j].insert(0, str(num))
                            entries[i][j].config(bg="#c8e6c9")
                            root.update()
                            time.sleep(0.05)
                        if solve_board(board, step_by_step):
                            return True
                        board[i][j] = 0
                        if step_by_step:
                            entries[i][j].delete(0, tk.END)
                            root.update()
                            time.sleep(0.05)
                return False
    return True

# Display solution on grid
def display_solution(board):
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal")
            entries[i][j].delete(0, tk.END)
            entries[i][j].insert(0, str(board[i][j]))
            entries[i][j].config(bg="white", fg="black")

# Solve the board
def solve(step_by_step=False):
    board = get_grid()
    if board:
        if solve_board(board, step_by_step):
            display_solution(board)
            messagebox.showinfo("Solved", "Sudoku puzzle solved successfully!")
        else:
            messagebox.showerror("Unsolvable", "No solution exists for this puzzle.")

# Clear board
def clear():
    for i in range(9):
        for j in range(9):
            entries[i][j].config(state="normal")
            entries[i][j].delete(0, tk.END)
            entries[i][j].config(bg="white", fg="black")

# --------- PUZZLE GENERATOR ---------
def fill_board(board):
    numbers = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if fill_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def generate_puzzle(empty_cells=40):
    board = [[0]*9 for _ in range(9)]
    fill_board(board)
    count = empty_cells
    while count > 0:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if board[i][j] != 0:
            board[i][j] = 0
            count -= 1
    return board

def load_puzzle():
    clear()
    puzzle = generate_puzzle(empty_cells=40)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                entries[i][j].insert(0, str(puzzle[i][j]))
                entries[i][j].config(fg="blue", state="disabled")

# Buttons
btn_frame = tk.Frame(root, bg="white")
btn_frame.grid(row=10, column=0, columnspan=9, pady=20)

tk.Button(btn_frame, text="Generate Puzzle", command=load_puzzle,
          bg="#FF9800", fg="white", font=('Arial', 12), padx=10).grid(row=0, column=0, padx=10)

tk.Button(btn_frame, text="Solve Instantly", command=lambda: solve(False),
          bg="#4CAF50", fg="white", font=('Arial', 12), padx=10).grid(row=0, column=1, padx=10)

tk.Button(btn_frame, text="Solve Step-by-Step", command=lambda: solve(True),
          bg="#2196F3", fg="white", font=('Arial', 12), padx=10).grid(row=0, column=2, padx=10)

tk.Button(btn_frame, text="Clear", command=clear,
          bg="#f44336", fg="white", font=('Arial', 12), padx=10).grid(row=0, column=3, padx=10)

root.mainloop()
