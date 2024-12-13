def part2():
    puzzle_input_file = open("day4_input.txt", "r")

    array = []
    for line in puzzle_input_file:
        array.append(line)

    word = "XMAS"

    result = 0
    for row in range(1, len(array) - 1):
        for col in range(1, len(array[row]) - 1):
            result = result + find_xmas(array, word, row, col)

    print(result)


def find_xmas(array, word, row, col):
    if array[row][col] != 'A':
        return False
    if ((array[row - 1][col - 1] == 'M' and array[row + 1][col + 1] == 'S') or
        (array[row - 1][col - 1] == 'S' and array[row + 1][col + 1] == 'M')):
        if ((array[row + 1][col - 1] == 'M' and array[row - 1][col + 1] == 'S') or
            (array[row + 1][col - 1] == 'S' and array[row - 1][col + 1] == 'M')):
            return 1
    return 0



def part1():
    puzzle_input_file = open("day4_input.txt", "r")

    array = []
    for line in puzzle_input_file:
        array.append(line)

    word = "XMAS"

    result = 0
    for row in range(0, len(array)):
        for col in range(0, len(array[row])):
            result = result + find_word(array, word, row, col)

    print(result)

def find_word(array, word, row, col):
    if array[row][col] != word[0]:
        return False
    result = 0
    if search_right(array, word, row, col):
        result = result + 1
    if search_left(array, word, row, col):
        result = result + 1
    if search_top(array, word, row, col):
        result = result + 1
    if search_bot(array, word, row, col):
        result = result + 1
    if search_top_left(array, word, row, col):
        result = result + 1
    if search_top_right(array, word, row, col):
        result = result + 1
    if search_bot_right(array, word, row, col):
        result = result + 1
    if search_bot_left(array, word, row, col):
        result = result + 1
    return result


def search_right(array, word, row, col):
    index = 1
    while index < len(word) and (col + index) < len(array[row]):
        if array[row][col + index] != word[index]:
            break
        index = index + 1
    return index == len(word)

def search_left(array, word, row, col):
    index = 1
    while index < len(word) and (col - index) >= 0:
        if array[row][col - index] != word[index]:
            break
        index = index + 1
    return index == len(word)

def search_top(array, word, row, col):
    index = 1
    while index < len(word) and (row - index) >= 0:
        if array[row - index][col] != word[index]:
            break
        index = index + 1
    return index == len(word)

def search_bot(array, word, row, col):
    index = 1
    while index < len(word) and (row + index) < len(array):
        if array[row + index][col] != word[index]:
            break
        index = index + 1
    return index == len(word)

def search_top_left(array, word, row, col):
    index = 1
    while index < len(word) and (row - index) >= 0 and (col - index) >= 0:
        if array[row - index][col - index] != word[index]:
            break
        index = index + 1
    return index == len(word)

def search_top_right(array, word, row, col):
    index = 1
    while index < len(word) and (row - index) >= 0 and (col + index) < len(array[row]):
        if array[row - index][col + index] != word[index]:
            break
        index = index + 1
    return index == len(word)

def search_bot_right(array, word, row, col):
    index = 1
    while index < len(word) and (row + index) < len(array) and (col + index) < len(array[row]):
        if array[row + index][col + index] != word[index]:
            break
        index = index + 1
    return index == len(word)

def search_bot_left(array, word, row, col):
    index = 1
    while index < len(word) and (row + index) < len(array) and (col - index) >= 0:
        if array[row + index][col - index] != word[index]:
            break
        index = index + 1
    return index == len(word)

part2()