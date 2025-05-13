import sys
import heapq


# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]

class GlobalProcess:
    def __init__(self, data):
        self.data = data

    def robot_scan_map(self, start, collected_keys):
        distances = [[None] * len(self.data[i]) for i in range(len(self.data))]
        distances[start[0]][start[1]] = 0
        queue = [(0, start)]
        step_dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        keys_to_found = []
        
        while queue:
            current_distance, current_position = heapq.heappop(queue)
            cx, cy = current_position[0], current_position[1]

            if self.data[cx][cy] in keys_char:
                if self.data[cx][cy] not in collected_keys:
                    keys_to_found.append({
                        'distance': current_distance,
                        'position': (cx, cy),
                        'key_char': self.data[cx][cy]
                    })
                    continue

            for dx, dy in step_dirs:
                nx = cx + dx
                ny = cy + dy
                distance = current_distance + 1

                if (self.data[nx][ny] != '.' \
                    and self.data[nx][ny] not in keys_char \
                    and not (self.data[nx][ny] in doors_char and self.data[nx][ny].lower() in collected_keys)) \
                    or distances[nx][ny] != None:
                    continue

                distances[nx][ny] = distance
                heapq.heappush(queue, (distance, (nx, ny)))
        return keys_to_found

    def main_process(self):
        robot_positions = []
        keys = []

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                c = self.data[i][j]
                if c == '@':
                    robot_positions.append((i, j))
                elif c in keys_char:
                    keys.append(c)

        keys = set(keys)
        queue = [(0, tuple(robot_positions), [])]
        min_dist = float('inf')
        visited = {}
        bellman_cache = {}

        while queue:
            current_distance, robots, collected_keys = heapq.heappop(queue)
            layout = (robots, tuple(sorted(collected_keys)))

            if layout in bellman_cache:
                continue

            if set(collected_keys) == keys:
                min_dist = min(min_dist, current_distance)
                bellman_cache[layout] = min_dist
                continue
            
            bellman_cache[layout] = current_distance
            for i in range(len(robots)):
                current_map_situation =  self.robot_scan_map(robots[i], collected_keys)
                for another_key in current_map_situation:
                    moved_to = list(robots)
                    moved_to[i] = another_key['position']
                    moved_to = tuple(moved_to)

                    current_collected_keys = list(collected_keys)
                    current_collected_keys.append(another_key['key_char'])

                    new_distance = current_distance + another_key['distance']
                    current_layout = (moved_to, tuple(sorted(current_collected_keys)))

                    if current_layout not in visited or new_distance < visited[current_layout]:
                        visited[current_layout] = new_distance
                        heapq.heappush(queue, (new_distance, moved_to, current_collected_keys))
        return min_dist

def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]

def solve(data):
    process = GlobalProcess(data)
    result = process.main_process()
    return result


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()