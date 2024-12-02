import pygame
from hill import run_game as train_hill
from rat import run_game as train_tracking
from Astart import run_game as train_astart
from BFS import run_game as train_bfs
# Kích thước màn hình
WIDTH, HEIGHT = 800, 600

# Màu sắc
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (100, 200, 100)  # Màu khi hover
screen_hill = pygame.display.set_mode((800,600))

# Khởi tạo Pygame
pygame.init()

# Tạo font chữ
font = pygame.font.Font(None, 50)

# Hàm hiển thị menu với 5 nút bấm
def draw_menu(screen, hover_index=None):
    screen.fill(BLACK)
    button_rects = []
    button_texts = ["Quit", "Hill Climbing Mode", "BackTracking Mode", "A-start Mode", "BFS Mode"]
    button_width, button_height = WIDTH // 2, 60
    spacing = 20
    start_y = HEIGHT // 2 - ((len(button_texts) - 1) * (button_height + spacing)) // 2

    for i, text in enumerate(button_texts):
        button_rect = pygame.Rect(WIDTH // 4, start_y + i * (button_height + spacing), button_width, button_height)
        # Vẽ nút với màu sắc hover nếu chuột nằm trên nút
        if i == hover_index:
            pygame.draw.rect(screen, HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, GREEN, button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 3)  # Viền trắng, độ dày 3 pixel
        
        button_rects.append(button_rect)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    return button_rects

# Chương trình chính
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu with 5 Buttons")
    running = True
    hover_index = None

    while running:
        button_rects = draw_menu(screen, hover_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Kiểm tra chuột đang hover trên nút nào
                hover_index = next((i for i, rect in enumerate(button_rects) if rect.collidepoint(event.pos)), None)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        print(f"Button {i + 1} clicked!")
                        # Gọi hàm tương ứng khi nút được click
                        if i == 0:
                            game_1()  # Chạy trò chơi 1
                        elif i == 1:
                            game_2()  # Gọi hàm cho trò chơi 2
                        elif i == 2:
                            game_3()  # Gọi hàm cho trò chơi 3
                        elif i == 3:
                            game_4()  # Gọi hàm cho trò chơi 4
                        elif i == 4:
                            game_5()  # Gọi hàm cho trò chơi 5

    pygame.quit()

# Hàm giả lập các trò chơi (cần định nghĩa các hàm này)
def game_1():
    pygame.quit()

def game_2():
    train_hill(screen_hill, "game_play_data.txt", algorithm_name="Hill Climbing")

def game_3():
    train_tracking()

def game_4():
    train_astart(screen_hill)

def game_5():
    train_bfs(screen_hill, "game_results.txt", algorithm_name="BFS")

if __name__ == "__main__":
    main()
