import matplotlib.pyplot as plt

def read_puzzle_steps(filename):
    steps = []
    current_step = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "":
                if current_step:
                    steps.append(current_step)
                    current_step = []
            else:
                current_step.append([int(num) if num != '.' else -1 for num in line.split()])

    if current_step:
        steps.append(current_step)

    return steps

def compute_filled_cells(steps):
    filled_cells = []
    for step in steps:
        count = sum(1 for row in step for cell in row if cell != -1)
        filled_cells.append(count)
    return filled_cells

def generate_graph():
    steps = read_puzzle_steps("puzzle_steps.txt")
    filled_cells = compute_filled_cells(steps)

    plt.figure()
    plt.plot(range(len(filled_cells)), filled_cells, label='Filled Cells Over Time', marker='o')
    plt.xlabel('Step')
    plt.ylabel('Number of Filled Cells')
    plt.title('Sudoku Solver Process')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    generate_graph()
