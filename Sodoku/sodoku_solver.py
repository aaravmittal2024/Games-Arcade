# Sodoku Solver (Using Backtracking Algorithm)

def is_valid_move(grid, row, col, number):
    """Checks if the given number can be placed at the specified row and col in the Sudoku grid."""

    # Check the given number in the current row.
    for x in range(9):
        if grid[row][x] == number:
            return False

    # Check the given number in the current column.
    for x in range(9):
        if grid[x][col] == number:
            return False
    
    # Identify the 3x3 grid the cell belongs to.
    corner_row = row - row % 3
    corner_col = col - col % 3
    
    # Check the given number in the 3x3 grid.
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == number:
                return False
    
    # If the number is not found in the row, column, and the 3x3 grid, then it's a valid move.
    return True 

def solve(grid, row=0, col=0):
    """Recursive function to solve the Sudoku puzzle using backtracking. """
    
    # If the column index is 9, we've reached the end of the row.
    if col == 9:
        # If it's also the last row, the puzzle is solved.
        if row == 8:
            return True 
        # Move to the next row and reset column index.
        row += 1
        col = 0
    
    # If the current cell is already filled, move to the next cell.
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)
    
    # Try numbers from 1 to 9 for the current cell.
    for num in range(1, 10):
        if is_valid_move(grid, row, col, num):
            grid[row][col] = num
            
            # Recurse with the next cell. If it returns True, the current cell number is valid.
            if solve(grid, row, col + 1):
                return True 
    
        # If no number is valid, reset the cell and backtrack.
        grid[row][col] = 0
    
    # Return False if no solution is found for the current cell.
    return False 



# Test Case 
grid = [[0,7,5,0,9,0,0,0,6],
        [0,2,3,0,8,0,0,4,0],
        [8,0,0,0,0,3,0,0,1],
        [5,0,0,7,0,2,0,0,0],
        [0,4,0,8,0,6,0,2,0],
        [0,0,0,9,0,1,0,0,3],
        [9,0,0,4,0,0,0,0,7],
        [0,6,0,0,7,0,5,8,0],
        [7,0,0,0,1,0,3,9,0]]

if solve(grid,0,0):
    for i in range(9):
        for j in range(9):
            print(grid[i][j], end=" ")
        print()
else:
    print("No Solution")
        