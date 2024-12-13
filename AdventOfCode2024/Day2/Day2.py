puzzle_input_file = open("day2_input.txt", "r")

nb_safe = 0
for line in puzzle_input_file:
    safe = True
    tokens = list(map(int, line.split()))
    direction = tokens[1] - tokens[0]
    abs_direction = abs(direction)
    if (abs_direction < 1) or (abs_direction > 3):
        continue
    prev_x = tokens[1]
    for x in tokens[2:]:
        gap = x - prev_x
        if (direction < 0 <= gap) or (direction > 0 >= gap):
            safe = False
            break
        abs_gap = abs(gap)
        if (abs_gap < 1) or (abs_gap > 3):
            safe = False
            break
        prev_x = x
    if safe:
        nb_safe = nb_safe + 1
        #print('{0} -> {1}'.format(tokens, safe))


print(nb_safe)

def is_safe(local_diff_array):
    #print(local_diff_array)
    prev_diff = 0
    for i in range(0, len(local_diff_array)):
        abs_local_diff = abs(local_diff_array[i])
        if abs_local_diff < 1 or abs_local_diff > 3:
            return i
        if prev_diff == 0:
            prev_diff = local_diff_array[i]
            continue
        if (prev_diff > 0 > local_diff_array[i]) or (prev_diff < 0 < local_diff_array[i]):
            return i
    return -1

def add_and_check(local_diff_array, check_index, side):
    a = check_index if side == "left" else check_index + 1
    b = check_index - 1 if side == "left" else check_index
    new_val = local_diff_array[a] + local_diff_array[b]
    new_list = local_diff_array.copy()
    new_list.pop(a)
    new_list[b] = new_val
    return is_safe(new_list)

puzzle_input_file = open("day2_input.txt", "r")

nb_safe = 0
for line in puzzle_input_file:
    safe = True
    diff_array = []
    tokens = list(map(int, line.split()))
    for i in range(1, len(tokens)):
        diff_array.append(tokens[i] - tokens[i-1])
    last_index = len(diff_array) - 1
    check = is_safe(diff_array)
    if check > -1:
        if (check <= 1 and is_safe(diff_array[1:]) < 0) or (check == last_index and is_safe(diff_array[:-1]) < 0):
            safe = True
        elif check == 0 or add_and_check(diff_array, check, "left") > -1:
            if check == last_index:
                safe = False
            elif add_and_check(diff_array, check, "right") > -1:
                safe = False
    if safe:
        nb_safe = nb_safe + 1

print(nb_safe)






