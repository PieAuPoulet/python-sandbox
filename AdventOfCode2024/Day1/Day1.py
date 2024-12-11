puzzle_input_file = open("day1_input.txt", "r")
left = []
right = []
for line in puzzle_input_file:
    tokens = line.split()
    left.append(tokens[0])
    right.append(tokens[1])
left.sort()
right.sort()

# print(left)
# print(right)

result = 0
for (l, r) in zip(left, right):
    result += abs(int(l) - int(r))
print(result)

def increase_dict(dictionary, number):
    nb_occurrences = dictionary.get(number, 0)
    nb_occurrences = nb_occurrences + 1
    dictionary[number] = nb_occurrences

dict_of_right_occurrences = {}
dict_of_left_occurrences = {}
for (l, r) in zip(left, right):
    increase_dict(dict_of_left_occurrences, int(l))
    increase_dict(dict_of_right_occurrences, int(r))

result = 0
for key, value in dict_of_left_occurrences.items():
    nb_right_occurrences = dict_of_right_occurrences.get(key, 0)
    result += key * nb_right_occurrences * value

print(result)



