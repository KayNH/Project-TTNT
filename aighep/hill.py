import pygame
import random
import time
import os

# Kích thước màn hình và ô
CELL_SIZE = 20
WIDTH, HEIGHT = 800, 600

# Màu sắc
GREEN = (234, 216, 192)
RED = (255, 241, 0)
BLACK = (0, 0, 0)
GRAY = (204, 43, 82)

# Hàm tính Manhattan Distance
def manhattan_distance(head, food):
    return abs(head[0] - food[0]) + abs(head[1] - food[1])

# Hàm ghi dữ liệu vào file
def log_results(filename, algorithm, play_count, score, elapsed_time):
    with open(filename, 'a+') as file:
        file.write(f"Play {play_count}, Algorithm: {algorithm}, Score: {score}, Time: {elapsed_time} s\n")

# Hàm đọc số lần chơi từ file
def read_play_count(filename):
    if not os.path.exists(filename):
        return 0
    with open(filename, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1]
            if "Play" in last_line:
                # Extract the play count from the last line
                play_count = int(last_line.split(',')[0].split()[1])
                return play_count + 1
    return 1  # Nếu file rỗng hoặc không tồn tại, bắt đầu từ 1

# Hàm chạy trò chơi
def run_game(screen, filename, algorithm_name="Hill Climbing"):
    clock = pygame.time.Clock()
    snake = [(400, 300)]
    food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
    direction = (0, 0)

    # Tạo chướng ngại vật
    obstacles = []
    for _ in range(30):
        obstacle = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        while obstacle == food or obstacle in snake:
            obstacle = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        obstacles.append(obstacle)

    running = True
    start_time = time.time()
    score = 0

    # Đọc số lần chơi từ file và tăng lên 1
    play_count = read_play_count(filename)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Tìm nước đi tốt nhất (Hill Climbing)
        head = snake[0]
        moves = [(0, -CELL_SIZE), (0, CELL_SIZE), (-CELL_SIZE, 0), (CELL_SIZE, 0)]
        best_move = direction
        min_distance = float('inf')

        for move in moves:
            new_head = (head[0] + move[0], head[1] + move[1])
            if (new_head not in snake
                    and new_head not in obstacles
                    and 0 <= new_head[0] < WIDTH
                    and 0 <= new_head[1] < HEIGHT):
                distance = manhattan_distance(new_head, food)
                if distance < min_distance:
                    min_distance = distance
                    best_move = move

        # Di chuyển rắn
        direction = best_move
        new_head = (head[0] + direction[0], head[1] + direction[1])
        snake.insert(0, new_head)

        # Ăn thức ăn
        if new_head == food:
            food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                    random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            while food in obstacles or food in snake:
                food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            score += 1
        else:
            snake.pop()

        # Kết thúc game nếu rắn tự cắn mình hoặc chạm chướng ngại vật
        if new_head in snake[1:] or new_head in obstacles:
            running = False

        # Vẽ màn hình
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))
        for obstacle in obstacles:
            pygame.draw.rect(screen, GRAY, (*obstacle, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (*food, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()

        clock.tick(10)

    elapsed_time = int(time.time() - start_time)
    log_results(filename, algorithm_name, play_count, score, elapsed_time)

# Khởi động trò chơi
