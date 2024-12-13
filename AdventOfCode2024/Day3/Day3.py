import re

def compute_sum(input_data):
    matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input_data)
    total_sum = 0
    for match in matches:
        num1 = int(match[0])
        num2 = int(match[1])
        product = num1 * num2
        total_sum += product
    return total_sum


puzzle_input_file = open("day3_input.txt", "r").read()
result = compute_sum(puzzle_input_file)

print(f"The sum of all products is: {result}")

dont_string = "don't()"
do_string = "do()"
result = 0
current_string = puzzle_input_file
current_index = 0
do = True
while current_index < len(puzzle_input_file):
    if do:
        next_stop = current_string.find(dont_string)
        if next_stop != -1:
            current_string = puzzle_input_file[current_index:(current_index + next_stop)]
            current_index = current_index + next_stop + len(dont_string)
        else:
            current_index = len(puzzle_input_file)
        result += compute_sum(current_string)
        #print(current_string)
        #print(result)
    else:
        next_stop = current_string.find(do_string)
        if next_stop != -1:
            current_index = current_index + next_stop + len(do_string)
        else:
            current_index = len(puzzle_input_file)
    do = not do
    current_string = puzzle_input_file[current_index:]
    #print(current_string)
print(result)


