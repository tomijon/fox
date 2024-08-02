"""Program that generates a wordsearch only containing the letters in
the word fox, without the word appearing in the wordsearch.

Author: Thomas Johnson
Created: 02/08/2024
Last Edit: 02/08/2024
"""
from sys import stderr
from random import shuffle, choice
from time import time as current_time


def display(wordsearch):
    """Outputs the wordsearch to stdout in a pretty and readable
    format."""
    for row in wordsearch:
        print(" ".join(row))


def surrounding(wordsearch, x, y):
    """Finds the letters contained in a 3x3 area around the x, y
    coordinate. Places "#" if the edge of the grid is reached.
    """
    neighbors = [["#" for _ in range(3)] for _ in range(3)]
    
    for x_off in range(-1, 2):
        if not 0 <= x + x_off < len(wordsearch):
            continue
        for y_off in range(-1, 2):
            if not 0 <= y + y_off < len(wordsearch):
                continue

            # Fetching value.
            neighbors[y_off + 1][x_off + 1] = wordsearch[y + y_off][x + x_off]
    return neighbors


def find_fox(grid):
    """Attempts to find the word fox in the grid. Grid size is expected
    to be 3x3.
    """
    assert len(grid) == 3
    assert len(grid[0]) == 3

    mix = False

    # Horrizontal Check.
    for row in grid:
        strrow = "".join(row)
        if strrow == "fox" or strrow == "xof":
            mix = True      

    # Vertical Checks.
    for x in range(3):
        strrow = "".join([grid[y][x] for y in range(3)])
        if strrow == "fox" or strrow == "xof":
            mix = True

    # Diagonal Checks.
    tlbr = grid[0][0] + grid[1][1] + grid[2][2]
    bltr = grid[2][0] + grid[1][1] + grid[0][2]

    if tlbr == "fox" or tlbr == "xof":
        mix = True
    if bltr == "fox" or bltr == "xof":
        mix = True
    return mix
    

def generate(size):
    """Generates an unsolvable fox wordsearch in a 2D array."""
    letters = list("fox")
    wordsearch = [[choice(letters) for _ in range(size)] for _ in range(size)]

    # Remove duplicates.
    shuffled = True
    while shuffled:
        shuffled = False
        
        for y in range(size):
            for x in range(size):
                neighbors = surrounding(wordsearch, x, y)
                is_fox = find_fox(neighbors)
                if is_fox:
                    wordsearch[y][x] = choice(letters)
                    shuffled = True
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
    
    display(wordsearch)
    print(f"Generated in {round((end - start) * 1000)}ms")
