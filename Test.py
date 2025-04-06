# Recursive function to find a path in a maze
def find_path(maze, x, y, path):
    # Get the dimensions of the maze
    rows, cols = len(maze), len(maze[0])

    # Base case: If (x, y) is the bottom-right corner, return True
    if x == rows - 1 and y == cols - 1:
        path.append((x, y))
        return True

    # Check if the current position is valid (within bounds and not a wall)
    if x >= 0 and y >= 0 and x < rows and y < cols and maze[x][y] == 0:
        # Mark the current position as part of the path
        path.append((x, y))

        # Mark the current cell as visited to avoid loops
        maze[x][y] = 2  # Any value other than 0 or 1 will do

        # Recursively explore the neighboring cells (down, right, up, left)
        if find_path(maze, x + 1, y, path):  # Move down
            return True
        if find_path(maze, x, y + 1, path):  # Move right
            return True
        if find_path(maze, x - 1, y, path):  # Move up
            return True
        if find_path(maze, x, y - 1, path):  # Move left
            return True

        # If no path is found, backtrack and remove the current position
        path.pop()

    # Return False if there's no valid path from this position
    return False


# Example usage:
maze = [
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 0, 1],
    [1, 1, 0, 0]
]

path = []
if find_path(maze, 0, 0, path):
    print("Path found:", path)
else:
    print("No path found")
