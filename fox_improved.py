"""Program that generates a wordsearch only containing the letters in
the word fox, without the word appearing in the wordsearch.

Author: Thomas Johnson
Created: 02/08/2024
Last Edit: 02/08/2024
"""
from sys import stderr
from random import choice, shuffle
from time import time as current_time


def display(wordsearch):
    """Outputs the wordsearch to stdout in a pretty and readable
    format."""
    for row in wordsearch:
        print(" ".join(row))


def surrounding(wordsearch, x, y):
    """Finds the letters contained in a 5x5 area around the x, y
    coordinate. Places "#" if the edge of the grid is reached.
    """
    neighbors = [["#" for _ in range(5)] for _ in range(5)]
    
    for x_off in range(-2, 3):
        if not 0 <= x + x_off < len(wordsearch):
            continue
        for y_off in range(-2, 3):
            if not 0 <= y + y_off < len(wordsearch):
                continue

            # Fetching value.
            neighbors[y_off + 2][x_off + 2] = wordsearch[y + y_off][x + x_off]
    return neighbors


def find_fox(grid):
    """Attempts to find the word fox in the grid. Grid size is expected
    to be 5x5.
    """
    assert len(grid) == 5
    assert len(grid[0]) == 5

    mix = False

    # Horrizontal Check.
    for row in grid:
        strrow = "".join(row)
        if "fox" in strrow or "xof" in strrow:
            return True      

    # Vertical Checks.
    for x in range(3):
        strrow = "".join([grid[y][x] for y in range(3)])
        if "fox" in strrow or "xof" in strrow:
            return True

    # Diagonal Checks.
    tlbr = grid[0][0] + grid[1][1] + grid[2][2]
    bltr = grid[2][0] + grid[1][1] + grid[0][2]

    if "fox" in tlbr or "xof" in tlbr:
        return True
    if "fox" in bltr or "xof" in bltr:
        return True
    return False


def distribution(wordsearch):
    """Determines the distribution of the 3 letters.
    Returns a dictionary with percentages (sum = 1)"""
    dist = {key: 0 for key in "fox"}
    for row in wordsearch:
        for value in row:
            dist[value] += 1

    for key in "fox":
        dist[key] /= (len(wordsearch) ** 2)
    return dist
    

def generate(size):
    """Generates an unsolvable fox wordsearch in a 2D array."""
    letters = list("fox")
    wordsearch = [["o" for _ in range(size)] for _ in range(size)]
    targets = [(x, y) for x in range(size) for y in range(size)]
    shuffle(targets)
    targets = targets[:round(len(targets) / 1.4)]

    while len(targets) > 0:
        x, y = targets.pop(-1)
        neighbors = surrounding(wordsearch, x, y)
        insert = choice(["f", "x"])

        # First attempt.
        neighbors[2][2] = insert
        if not find_fox(neighbors):
            wordsearch[y][x] = insert
            continue

        # Second attempt.
        neighbors[2][2] = "f" if insert == "x" else "x"
        if not find_fox(neighbors):
            wordsearch[y][x] = "f" if insert == "x" else "x"
            continue
    return wordsearch


if __name__ == "__main__":
    while True:
        print("Enter grid size >> ", end="")
        try:
            size = int(input())
            break
        except: print("Please enter a whole number.", file=stderr, flush=True)

    # Timing execution
    start = current_time()
    wordsearch = generate(size)
    end = current_time()

    print()
    display(wordsearch)
    print()

    # Distribution.
    print("Distribution of letters: ")
    dist = distribution(wordsearch)
    for key in "fox":
        print(f"{key}: {round(dist[key] * 100)}%")
    
    print(f"Generated in {round((end - start) * 1000)}ms")

    # Calculate average distribution.
    total = {key: 0 for key in "fox"}
    for i in range(1000):
        wordsearch = generate(size)
        dist = distribution(wordsearch)
        for key in "fox":
            total[key] += dist[key]

    print("\nAverage Distribution (1000 runs): ")
    for key in "fox":
        print(f"{key}: {round(total[key] / 1000 * 100)}%")
