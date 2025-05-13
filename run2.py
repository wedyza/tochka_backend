import sys
import re
import heapq

# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]
regexp = r'[^@\#a-zA-Z\.]'

class Statement:
    def __init__(self, pos, collected_doors = []):
        self.position = pos
        self.doors = collected_doors

    def __lt__(self, obj):
        return self.position < obj.position
    
    def __str__(self):
        return f'{self.position} {self.doors} {self.__hash__}'


class Robot:
    def __init__(self, initial_pos):
        self.keys = {}
        self.doors = {}
        self.initial_pos = initial_pos


class Walker:
    def __init__(self, initial_pos):
        self.pos = initial_pos
        self.distance = 0


class GlobalProcess:
    def __init__(self, robots, data):
        self.robots = robots
        self.data = data
        self.collected_keys = []
        self.operate_keys()
        self.create_walkers()


    def robot_walk_to(self, robot:Walker, target_pos):
        start = robot.pos
        distances = [[float('inf')] * len(self.data[i]) for i in range(len(self.data))]
        distances[start[0]][start[1]] = 0
        queue = [(0, start)]
        map_length = len(distances)
        map_width = len(distances[0])
        step_dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while queue:
            current_distance, current_position = heapq.heappop(queue)
            if current_position == target_pos:
                robot.pos = target_pos
                robot.distance += current_distance
                return robot

            if current_distance > distances[current_position[0]][current_position[1]]:
                continue
            
            for dx, dy in step_dirs:
                nx = current_position[0] + dx
                ny = current_position[1] + dy

                if nx >= map_length or ny >= map_width or (self.data[nx][ny] != '.' and self.data[nx][ny] not in keys_char and self.data[nx][ny].lower() not in self.collected_keys):
                    continue
                distance = current_distance + 1

                if distance <= distances[nx][ny]:
                    distances[nx][ny] = distance
                    heapq.heappush(queue, (distance, (nx, ny)))

    def create_walkers(self):
        self.walkers = []
        for robot in self.robots:
            self.walkers.append(Walker(robot.initial_pos))

    def operate_keys(self):
        self.keys_behind_doors = []
        self.keys_without_doors = []
        for c, robot in enumerate(self.robots):
            for key in robot.keys.keys():
                if len(robot.keys[key]['doors']) == 0:
                    self.keys_without_doors.append({
                        'key_char': key,
                        'position': robot.keys[key]['position'],
                        'robot': c
                    })
                else:
                    self.keys_behind_doors.append({
                        'key_char': key,
                        'position': robot.keys[key]['position'],
                        'doors': robot.keys[key]['doors'],
                        'robot': c
                    })


    def reoperate_keys(self):
        for key in self.keys_behind_doors:
            for door in key['doors']:
                if door.lower() in self.collected_keys:
                    key['doors'].remove(door)
                if len(key['doors']) == 0:
                    self.keys_without_doors.append(key)
                    self.keys_behind_doors.remove(key)
    

    def calculate_distance(self):
        answer = 0
        for walker in self.walkers:
            answer += walker.distance
        return answer


    def main_process(self):
        while True:
            for another_key in self.keys_without_doors:
                key_position = another_key['position']
                key_char = another_key['key_char']
                robot_id = another_key['robot']

                walker = self.walkers[robot_id]
                self.robot_walk_to(walker, key_position)
                self.collected_keys.append(key_char)
                self.keys_without_doors.remove(another_key)

            if len(self.keys_behind_doors) == 0 and len(self.keys_without_doors) == 0:
                return self.calculate_distance()
            
            self.reoperate_keys()

def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]

def print_map(map):
    for row in map:
        print(row)

def robot_scan_map(data, robot:Robot):
    distances = [[float('inf')] * len(data[i]) for i in range(len(data))]
    distances[robot.initial_pos[0]][robot.initial_pos[1]] = 0
    queue = [(0, Statement(robot.initial_pos, []))]

    map_length = len(distances)
    map_width = len(distances[0])
    step_dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while queue:
        current_distance, current_position = heapq.heappop(queue)

        if current_distance > distances[current_position.position[0]][current_position.position[1]]:
            continue
        
        for dx, dy in step_dirs:
            nx = current_position.position[0] + dx
            ny = current_position.position[1] + dy

            distance = current_distance + 1
            if nx >= map_length or ny >= map_width or (data[nx][ny] != '.' and data[nx][ny] not in keys_char and data[nx][ny] not in doors_char):
                continue

            if distance <= distances[nx][ny]:
                doors = current_position.doors.copy()
                if data[nx][ny] in keys_char:
                    robot.keys[data[nx][ny]] = {
                        'position': (nx, ny),
                        'doors': doors
                    }
                if data[nx][ny] in doors_char:
                    robot.doors[data[nx][ny]] = (nx, ny)
                    doors.append(data[nx][ny])
                
                distances[nx][ny] = distance
                heapq.heappush(queue, (distance, Statement((nx, ny), doors)))
    return robot

def solve(data):
    robot_positions = []

    for i in range(len(data)):
        for j in range(len(data[i])):
            c = data[i][j]
            if c == '@':
                robot_positions.append((i, j))
    robot_list = []
    for position in robot_positions:
        robot_list.append(robot_scan_map(data, Robot(position)))
    process = GlobalProcess(robot_list, data)
    answer = process.main_process()
    return answer


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()