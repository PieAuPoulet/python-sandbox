def part1():
    puzzle_input_file = open("day6_input.txt", "r")

    array = []

    y = 0
    start_position = ()
    for line in puzzle_input_file:
        line = line.replace('\n', '')
        array.append([])
        for x in range(0, len(line)):
            array[y].append(line[x])
            if line[x] == '^':
                start_position = (x, y)
        y = y + 1

    print(array)
    g = Guard(start_position, array)
    g.move()

    print(len(g.visited_positions))

class Guard:

    visited_positions = set()
    direction = (0, -1) # (x,y) vector
    position = ()

    def __init__(self, position, array):
        self.position = position
        self.array = array

    def move(self):
        #print(self.position)
        while True:
            self.visited_positions.add(self.position)
            next_y = self.position[1] + self.direction[1]
            next_x = self.position[0] + self.direction[0]
            if next_y < 0 or next_y >= len(self.array) or next_x < 0 or next_x >= len(self.array[0]):
                return
            next_square = self.array[next_y][next_x]
            if next_square == '#':
                x2 = -self.direction[1]
                y2 = self.direction[0]
                self.direction = (x2, y2)
            else:
                self.position = (next_x, next_y)

part1()






