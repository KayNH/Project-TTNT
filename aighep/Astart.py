import pygame
import heapq
import sys
import random
from collections import namedtuple
import time

# Define the game parameters
WIDTH, HEIGHT = 800, 600          # Window size
CELL_SIZE = 20                    # Size of each cell
COLS = WIDTH // CELL_SIZE         # Number of columns
ROWS = HEIGHT // CELL_SIZE        # Number of rows
FPS = 10

# Colors
WHITE = (255, 255, 255)
GREEN = (234, 216, 192)
RED = (255, 241, 0)
BLACK = (0, 0, 0)
GRAY = (204, 43, 82)

# Define positions
Point = namedtuple('Point', ['x', 'y'])

class Node:
    def __init__(self, position, parent=None, g_cost=0, h_cost=0):
        self.position = position
        self.parent = parent
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def __lt__(self, other):
        return self.f_cost < other.f_cost

# A* pathfinding algorithm
def astar(snake, food, walls):
    open_list = []
    closed_set = set()

    start_node = Node(snake[0], None, 0, heuristic(snake[0], food))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)
        if current_node.position == food:
            return reconstruct_path(current_node)

        closed_set.add(current_node.position)
        for neighbor in get_neighbors(current_node.position, walls):
            if neighbor in closed_set or neighbor in snake[1:] or neighbor in walls:
                continue

            new_g_cost = current_node.g_cost + 1
            neighbor_node = Node(neighbor, current_node, new_g_cost, heuristic(neighbor, food))
            
            if any(open_node.position == neighbor and open_node.f_cost <= neighbor_node.f_cost for open_node in open_list):
                continue

            heapq.heappush(open_list, neighbor_node)

    return []  # No path found

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

# Get valid neighboring cells
def get_neighbors(pos, walls):
    directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]
    neighbors = [Point(pos.x + d.x, pos.y + d.y) for d in directions]
    return [n for n in neighbors if 0 <= n.x < COLS and 0 <= n.y < ROWS and n not in walls]

# Reconstruct the path from the end node to the start
def reconstruct_path(node):
    path = []
    while node.parent is not None:
        dx = node.position.x - node.parent.position.x
        dy = node.position.y - node.parent.position.y
        if dx == 1:
            path.append('RIGHT')
        elif dx == -1:
            path.append('LEFT')
        elif dy == 1:
            path.append('DOWN')
        elif dy == -1:
            path.append('UP')
        node = node.parent
    return path[::-1]

# Generate random walls
def generate_walls():
    walls = set()
    while len(walls) < 30:  # 30 random walls
        wall = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        walls.add(wall)
    return walls

# Save data to a text file
def log_game_data(algorithm, play_time, score, play_count):
    with open('game_log.txt', 'a') as file:
        file.write(f"Game {play_count}: Algorithm: {algorithm}, Play Time: {play_time:.2f} seconds, Score: {score}\n")

# Get the current number of games played
def get_play_count():
    try:
        with open('games_played.txt', 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

# Increment the play count and save it
def increment_play_count():
    count = get_play_count() + 1
    with open('games_played.txt', 'w') as file:
        file.write(str(count))
    return count

# Run the game
def run_game(screen):
    clock = pygame.time.Clock()
    
    snake = [Point(5, 5)]
    direction = 'RIGHT'
    food = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    walls = generate_walls()

    start_time = time.time()
    moves = 0  # Score counter
    running = True

    while running:
        screen.fill(BLACK)
        
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # A* pathfinding
        path = astar(snake, food, walls)
        if path:
            direction = path[0]

        # Move the snake
        head = snake[0]
        if direction == 'UP':
            new_head = Point(head.x, head.y - 1)
        elif direction == 'DOWN':
            new_head = Point(head.x, head.y + 1)
        elif direction == 'LEFT':
            new_head = Point(head.x - 1, head.y)
        elif direction == 'RIGHT':
            new_head = Point(head.x + 1, head.y)
        
        snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == food:
            food = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            while food in walls or food in snake:
                food = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            moves += 1  # Increase score
        else:
            snake.pop()

        # Check for collisions
        if new_head.x < 0 or new_head.y < 0 or new_head.x >= COLS or new_head.y >= ROWS or new_head in snake[1:] or new_head in walls:
            running = False

        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, GRAY, pygame.Rect(wall.x * CELL_SIZE, wall.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the snake and food
        for segment in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, pygame.Rect(food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(FPS)

    # Log game data after the game ends
    end_time = time.time()
    play_time = end_time - start_time
    play_count = increment_play_count()
    log_game_data("A*", play_time, moves, play_count)

# Run the game loop

