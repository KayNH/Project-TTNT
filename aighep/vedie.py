import matplotlib.pyplot as plt

# Đọc dữ liệu từ các file
with open('game_log.txt', 'r') as file:
    lines_astar = file.readlines()

with open('game_play_data.txt', 'r') as file:
    lines_hill_climbing = file.readlines()

with open('game_results.txt', 'r') as file:
    lines_bfs = file.readlines()

# Khởi tạo danh sách để lưu điểm số của các thuật toán
scores_astar = []
scores_hill_climbing = []
scores_bfs = []

# Phân tích dữ liệu từ game_log.txt (A*)
for line in lines_astar:
    if 'Algorithm: A*' in line:
        try:
            # Tách phần điểm số từ dòng dữ liệu
            score_index = line.index('Score: ') + len('Score: ')
            score = int(line[score_index:line.find(' ', score_index)].strip())
            scores_astar.append(score)
        except (ValueError, IndexError):
            print(f"Skipping invalid line in game_log.txt: {line.strip()}")

# Phân tích dữ liệu từ game_play_data.txt (Hill Climbing)
for line in lines_hill_climbing:
    if 'Algorithm: Hill Climbing' in line:
        try:
            # Tách phần điểm số từ dòng dữ liệu
            score_index = line.index('Score: ') + len('Score: ')
            score = int(line[score_index:line.find(',', score_index)].strip())
            scores_hill_climbing.append(score)
        except (ValueError, IndexError):
            print(f"Skipping invalid line in game_play_data.txt: {line.strip()}")

# Phân tích dữ liệu từ game_results.txt (BFS)
for line in lines_bfs:
    if 'Algorithm: BFS' in line:
        try:
            # Tách phần điểm số từ dòng dữ liệu
            score_index = line.index('Score: ') + len('Score: ')
            score = int(line[score_index:line.find(',', score_index)].strip())
            scores_bfs.append(score)
        except (ValueError, IndexError):
            print(f"Skipping invalid line in game_results.txt: {line.strip()}")

# In ra số điểm đã phân tích để kiểm tra
print("Scores for A*:", scores_astar)
print("Scores for Hill Climbing:", scores_hill_climbing)
print("Scores for BFS:", scores_bfs)

# Vẽ biểu đồ
plt.figure(figsize=(12, 6))

# Vẽ đường biểu diễn điểm số của A*
if scores_astar:
    plt.plot(range(1, len(scores_astar) + 1), scores_astar, marker='o', linestyle='-', label='A*')

# Vẽ đường biểu diễn điểm số của Hill Climbing
if scores_hill_climbing:
    plt.plot(range(1, len(scores_hill_climbing) + 1), scores_hill_climbing, marker='x', linestyle='--', label='Hill Climbing')

# Vẽ đường biểu diễn điểm số của BFS
if scores_bfs:
    plt.plot(range(1, len(scores_bfs) + 1), scores_bfs, marker='s', linestyle='-.', label='BFS')

plt.title('Điểm số theo số lần chơi cho các thuật toán')
plt.xlabel('Số lần chơi')
plt.ylabel('Điểm số')
plt.legend()
plt.grid(True)
plt.show()
