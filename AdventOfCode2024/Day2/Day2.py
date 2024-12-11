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



