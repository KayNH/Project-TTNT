import pygame
import sys
import random
from collections import deque, namedtuple
import time

# Định nghĩa các thông số
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE
FPS = 10

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (234, 216, 192)
RED = (255, 241, 0)
BLACK = (0, 0, 0)
GRAY = (204, 43, 82)

# Định nghĩa vị trí
Point = namedtuple('Point', ['x', 'y'])

# Các ô lân cận hợp lệ
def get_neighbors(pos, walls):
    directions = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]
    neighbors = [Point(pos.x + d.x, pos.y + d.y) for d in directions]
    return [n for n in neighbors if 0 <= n.x < COLS and 0 <= n.y < ROWS and n not in walls]

# Hàm BFS tìm đường đi từ đầu rắn đến thức ăn
def bfs(snake, food, walls):
    queue = deque([(snake[0], [])])  # (vị trí hiện tại, đường đi)
    visited = set()
    visited.add(snake[0])

    while queue:
        current, path = queue.popleft()

        if current == food:
            return path

        for neighbor in get_neighbors(current, walls):
            if neighbor not in visited and neighbor not in snake[1:]:
                visited.add(neighbor)
                dx = neighbor.x - current.x
                dy = neighbor.y - current.y
                if dx == 1:
                    queue.append((neighbor, path + ['RIGHT']))
                elif dx == -1:
                    queue.append((neighbor, path + ['LEFT']))
                elif dy == 1:
                    queue.append((neighbor, path + ['DOWN']))
                elif dy == -1:
                    queue.append((neighbor, path + ['UP']))

    return []

# Hàm khởi tạo các tường ngẫu nhiên
def generate_walls():
    walls = set()
    while len(walls) < 30:
        wall = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        walls.add(wall)
    return walls

# Hàm ghi dữ liệu vào file
def log_results(filename, algorithm, play_count, score, elapsed_time):
    with open(filename, 'a+') as file:
        file.write(f"Play {play_count}, Algorithm: {algorithm}, Score: {score}, Time: {elapsed_time} s\n")

# Hàm đọc số lần chơi từ file
def get_play_count(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Lấy số lần chơi cuối cùng từ dòng cuối cùng
            if lines:
                last_line = lines[-1]
                play_count = int(last_line.split(",")[0].split()[1]) + 1
                return play_count
            else:
                return 1  # Nếu file rỗng, bắt đầu từ 1
    except FileNotFoundError:
        return 1  # Nếu file không tồn tại, bắt đầu từ 1

# Hàm chạy trò chơi
def run_game(screen, filename, algorithm_name="BFS"):
    play_count = get_play_count(filename)
    clock = pygame.time.Clock()

    snake = [Point(5, 5)]
    direction = 'RIGHT'
    food = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
    walls = generate_walls()
    score = 0
    start_time = time.time()
    running = True
    
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        path = bfs(snake, food, walls)  # Thay đổi nếu bạn muốn sử dụng thuật toán khác
        if path:
            direction = path[0]

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

        if new_head == food:
            food = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            while food in walls or food in snake:
                food = Point(random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            score += 1
        else:
            snake.pop()

        if new_head.x < 0 or new_head.y < 0 or new_head.x >= COLS or new_head.y >= ROWS or new_head in snake[1:] or new_head in walls:
            running = False

        for wall in walls:
            pygame.draw.rect(screen, GRAY, pygame.Rect(wall.x * CELL_SIZE, wall.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for segment in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, RED, pygame.Rect(food.x * CELL_SIZE, food.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        elapsed_time = int(time.time() - start_time)
        time_text = font.render(f'Time: {elapsed_time} s', True, WHITE)
        screen.blit(time_text, (WIDTH - 120, 10))

        pygame.display.flip()
        clock.tick(FPS)

    log_results(filename, algorithm_name, play_count, score, elapsed_time)

# Khởi động trò chơi

