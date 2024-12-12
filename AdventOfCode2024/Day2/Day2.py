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

def check_diff_array(local_diff_array):
    print(local_diff_array)
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

def check_left(local_diff_array, check_index):
    new_val = local_diff_array[check_index - 1] + local_diff_array[check_index]
    new_list = local_diff_array.copy()
    new_list.pop(check_index)
    new_list[check_index - 1] = new_val
    return check_diff_array(new_list)

def check_right(local_diff_array, check_index):
    new_val = local_diff_array[check_index + 1] + local_diff_array[check_index]
    new_list = local_diff_array.copy()
    new_list.pop(check_index + 1)
    new_list[check_index] = new_val
    return check_diff_array(new_list)

puzzle_input_file = open("day2_input.txt", "r")

nb_safe = 0
for line in puzzle_input_file:
    safe = True
    diff_array = []
    tokens = list(map(int, line.split()))
    for i in range(1, len(tokens)):
        diff_array.append(tokens[i] - tokens[i-1])
    check = check_diff_array(diff_array)
    if check <= 1 and check_diff_array(diff_array[1:]) < 0:
        #print("Wrong first")
        safe = True
    elif check == (len(diff_array) - 1) and check_diff_array(diff_array[:-1]) < 0:
        #print("Wrong last")
        safe = True
    elif check > -1:
        if check == 0:
            new_check = check
        else:
            new_check = check_left(diff_array, check)
        if new_check > -1:
            if check < (len(diff_array) - 1):
                new_check = check_right(diff_array, check)
                if new_check > -1:
                    safe = False
            else:
                safe = False
    if safe:
        nb_safe = nb_safe + 1

print(nb_safe)






