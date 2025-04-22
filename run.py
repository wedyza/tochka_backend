from datetime import datetime
import json

def check_capacity(max_capacity: int, guests: list) -> bool:
    timeline = []
    for another_guest in guests:
        timeline.append((datetime.strptime(another_guest['check-in'], '%Y-%m-%d'), 1))
        timeline.append((datetime.strptime(another_guest['check-out'], '%Y-%m-%d'), -1))
    
    timeline = sorted(timeline)
    curr_capacity = 0
    for day in timeline:
        curr_capacity += day[1]
        if curr_capacity > max_capacity:
            return False
    return True


if __name__ == "__main__":
    # Чтение входных данных
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)