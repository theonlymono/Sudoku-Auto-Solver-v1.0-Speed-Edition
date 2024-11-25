import tkinter as tk
from tkinter import messagebox
import subprocess

# Sudoku solving logic
def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None

def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True

def solve_sudoku(puzzle, original, steps):
    row, col = find_next_empty(puzzle)
    if row is None:
        return True

    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            if original[row][col] == -1:
                puzzle[row][col] = guess

                steps.append([row[:] for row in puzzle])  # Save the state of the puzzle
                if solve_sudoku(puzzle, original, steps):
                    return True
                puzzle[row][col] = -1
                steps.append([row[:] for row in puzzle])  # Save the state after reverting

    return False

# Check validity of the initial puzzle
def check_initial_validity(puzzle):
    for r in range(9):
        for c in range(9):
            num = puzzle[r][c]
            if num != -1:
                puzzle[r][c] = -1
                if not is_valid(puzzle, num, r, c):
                    puzzle[r][c] = num
                    return False
                puzzle[r][c] = num
    return True

# Extract puzzle from the GUI
def get_puzzle_from_gui():
    puzzle = []
    for r in range(9):
        row = []
        for c in range(9):
            cell_value = entries[r][c].get()
            if cell_value.isdigit():
                row.append(int(cell_value))
            else:
                row.append(-1)
        puzzle.append(row)
    return puzzle

# Show the solution in the GUI
def show_solution():
    puzzle = get_puzzle_from_gui()
    original_puzzle = [row[:] for row in puzzle]
    steps = []

    if not check_initial_validity(puzzle):
        messagebox.showerror("Invalid Puzzle", "This Sudoku puzzle contains conflicts.")
        return

    if solve_sudoku(puzzle, original_puzzle, steps):
        for r in range(9):
            for c in range(9):
                if original_puzzle[r][c] == -1:
                    entries[r][c].delete(0, tk.END)
                    entries[r][c].insert(0, str(puzzle[r][c]))
        
        # Save steps to a file for the graph viewer
        with open("puzzle_steps.txt", "w") as file:
            for step in steps:
                for row in step:
                    file.write(" ".join(str(num) if num != -1 else "." for num in row) + "\n")
                file.write("\n")
                
    else:
        messagebox.showerror("Unsolvable", "This Sudoku puzzle is unsolvable.")

def show_process():
    try:
        subprocess.run(["python", "graph_script.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred while trying to open the process viewer: {e}")

# Reset the grid
def reset_grid():
    for r in range(9):
        for c in range(9):
            entries[r][c].delete(0, tk.END)
    entries[0][0].focus()

# Validate user input
def validate_input(digit, row, col):
    if digit.isdigit() and 1 <= int(digit) <= 9:
        return True
    elif digit == "":
        return True
    else:
        return False

def move_to_next_cell(row, col):
    if col < 8:
        entries[row][col + 1].focus()
    elif row < 8:
        entries[row + 1][0].focus()

def move_to_previous_cell(row, col):
    if col > 0:
        entries[row][col - 1].focus()
    elif row > 0:
        entries[row - 1][8].focus()

def on_key_press(event, row, col):
    if event.char.isdigit() and 1 <= int(event.char) <= 9:
        entries[row][col].delete(0, tk.END)
        entries[row][col].insert(0, event.char)
        move_to_next_cell(row, col)
    return "break"

def on_backspace(event, row, col):
    if entries[row][col].get() == "":
        move_to_previous_cell(row, col)
    else:
        entries[row][col].delete(0, tk.END)
    return "break"

def on_arrow_key(event, row, col):
    if event.keysym == "Up" and row > 0:
        entries[row - 1][col].focus()
    elif event.keysym == "Down" and row < 8:
        entries[row + 1][col].focus()
    elif event.keysym == "Left" and col > 0:
        entries[row][col - 1].focus()
    elif event.keysym == "Right" and col < 8:
        entries[row][col + 1].focus()
    return "break"

def on_key_release(event, row, col):
    content = entries[row][col].get()
    if len(content) > 1:
        entries[row][col].delete(1, tk.END)

root = tk.Tk()
root.title("Sudoku Auto Completion: Speed Edition")

root.configure(bg="#F4F4F9")

frames = [[None for _ in range(3)] for _ in range(3)]
for r in range(3):
    for c in range(3):
        frame = tk.Frame(root, bg="#E0E0E0", bd=3, relief="solid")
        frame.grid(row=r, column=c, padx=5, pady=5)
        frames[r][c] = frame

font_style = ("Arial", 18, "bold")

entries = [[None for _ in range(9)] for _ in range(9)]
for r in range(9):
    for c in range(9):
        vcmd = (root.register(validate_input), '%P', r, c)
        entry = tk.Entry(frames[r // 3][c // 3], width=3, font=font_style, justify="center", validate="key", validatecommand=vcmd, bg="#FFFFFF", bd=2, relief="solid")
        entry.grid(row=r % 3, column=c % 3, padx=5, pady=5)
        entry.bind("<KeyPress>", lambda event, row=r, col=c: on_key_press(event, row, col))
        entry.bind("<KeyRelease>", lambda event, row=r, col=c: on_key_release(event, row, col))
        entry.bind("<BackSpace>", lambda event, row=r, col=c: on_backspace(event, row, col))
        entry.bind("<Up>", lambda event, row=r, col=c: on_arrow_key(event, row, col))
        entry.bind("<Down>", lambda event, row=r, col=c: on_arrow_key(event, row, col))
        entry.bind("<Left>", lambda event, row=r, col=c: on_arrow_key(event, row, col))
        entry.bind("<Right>", lambda event, row=r, col=c: on_arrow_key(event, row, col))
        entries[r][c] = entry

# solve_button = tk.Button(root, text="Solve", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=show_solution, bd=0, relief="solid")
# solve_button.grid(row=3, columnspan=3, pady=20)

# reset_button = tk.Button(root, text="Reset", font=("Arial", 14, "bold"), bg="#F44336", fg="white", command=reset_grid, bd=0, relief="solid")
# reset_button.grid(row=4, columnspan=3, pady=10)

# process_button = tk.Button(root, text="Show Process", font=("Arial", 14, "bold"), bg="#2196F3", fg="white", command=show_process, bd=0, relief="solid")
# process_button.grid(row=5, columnspan=3, pady=10)

solve_button = tk.Button(root, text="Solve", font=("Arial", 14, "bold"), command=show_solution, bg="#4CAF50", fg="white")
solve_button.grid(row=5, column=0, pady=20)

process_button = tk.Button(root, text="Show Process", font=("Arial", 14, "bold"), command=show_process, bg="#2196F3", fg="white")
process_button.grid(row=5, column=1, pady=20)

reset_button = tk.Button(root, text="Reset", font=("Arial", 14, "bold"), command=reset_grid, bg="#F44336", fg="white")
reset_button.grid(row=5, column=2, pady=20)

root.mainloop()
