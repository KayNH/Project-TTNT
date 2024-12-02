import matplotlib.pyplot as plt

# Đọc dữ liệu từ tệp game_log.txt (A*)
with open('game_log.txt', 'r') as file:
    lines_astar = file.readlines()

# Đọc dữ liệu từ tệp game_play_data.txt (Hill Climbing)
with open('game_play_data.txt', 'r') as file:
    lines_hill_climbing = file.readlines()

# Đọc dữ liệu từ tệp game_results.txt (BFS)
with open('game_results.txt', 'r') as file:
    lines_bfs = file.readlines()

# Khởi tạo danh sách để lưu thời gian chơi của các thuật toán
play_times_astar = []
play_times_hill_climbing = []
play_times_bfs = []

# Phân tích từng dòng từ game_log.txt để lấy dữ liệu A*
# Phân tích từng dòng từ game_log.txt để lấy dữ liệu A*
for line in lines_astar:
    if line.strip() and 'Algorithm: A*' in line:  # Kiểm tra thuật toán A*
        try:
            # Tách phần thời gian chơi từ chuỗi
            play_time = float(line.split('Play Time: ')[1].split('seconds')[0].strip())
            play_times_astar.append(play_time)
        except (IndexError, ValueError) as e:
            print(f"Invalid line format for A*: {line.strip()} - Error: {e}")


# Phân tích từng dòng từ game_play_data.txt để lấy dữ liệu Hill Climbing
for line in lines_hill_climbing:
    if line.strip() and 'Algorithm: Hill Climbing' in line:
        parts = line.split(',')
        if len(parts) > 2:  # Đảm bảo đủ phần tử
            play_time_part = parts[2].strip()  # Lấy phần thời gian chơi
            try:
                play_time = float(play_time_part.split(': ')[1].replace('s', '').strip())
                play_times_hill_climbing.append(play_time)
            except (IndexError, ValueError):
                print(f"Skipping invalid line in game_play_data.txt: {line.strip()}")

# Phân tích từng dòng từ game_results.txt để lấy dữ liệu BFS
for line in lines_bfs:
    if line.strip() and 'Algorithm: BFS' in line:
        parts = line.split(',')
        if len(parts) > 2:  # Đảm bảo đủ phần tử
            play_time_part = parts[2].strip()  # Lấy phần thời gian chơi
            try:
                play_time = float(play_time_part.split(': ')[1].replace('s', '').strip())
                play_times_bfs.append(play_time)
            except (IndexError, ValueError):
                print(f"Skipping invalid line in game_results.txt: {line.strip()}")

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))

# Vẽ đường biểu diễn thời gian chơi của A*
if play_times_astar:
    plt.plot(range(1, len(play_times_astar) + 1), play_times_astar, marker='o', linestyle='-', label='A*')

# Vẽ đường biểu diễn thời gian chơi của Hill Climbing
if play_times_hill_climbing:
    plt.plot(range(1, len(play_times_hill_climbing) + 1), play_times_hill_climbing, marker='x', linestyle='--', label='Hill Climbing')

# Vẽ đường biểu diễn thời gian chơi của BFS
if play_times_bfs:
    plt.plot(range(1, len(play_times_bfs) + 1), play_times_bfs, marker='s', linestyle='-.', label='BFS')

plt.title('Thời gian chơi theo số lần chơi cho các thuật toán')
plt.xlabel('Số lần chơi')
plt.ylabel('Thời gian chơi (giây)')
plt.legend()
plt.grid(True)
plt.show()
