

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

def part2():
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

    #print(array)
    g = Guard2(start_position, array, (0, -1))
    g.move(False, ())

    #print(len(g.visited_positions))

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

class Guard2:

    def __init__(self, position, array, direction):
        self.start_position = position
        self.position = position
        self.array = array
        self.direction = direction
        self.simulated_blocks = set()
        self.found_loop_blocks = set()
        self.encountered_simu_blocks = set()
        self.nb_simu_block_encounter = 0

    def move(self, simulating, simulated_block):
        #print("{0} {1} {2}".format(simulating, simulated_block, self.position))
        while True:
            next_y = self.position[1] + self.direction[1]
            next_x = self.position[0] + self.direction[0]
            if next_y < 0 or next_y >= len(self.array) or next_x < 0 or next_x >= len(self.array[0]):
                if not simulating:
                    self.found_loop_blocks.remove(self.start_position)
                    print(len(self.found_loop_blocks))
                return False
            next_square = self.array[next_y][next_x]
            if next_square == '#' or (simulating and (next_x, next_y) == simulated_block):
                if simulating:
                    if (next_x, next_y, self.direction) in self.encountered_simu_blocks:
                        return True
                    else:
                        self.encountered_simu_blocks.add((next_x, next_y, self.direction))
                x2 = -self.direction[1]
                y2 = self.direction[0]
                self.direction = (x2, y2)
            else:
                if not simulating:
                    if (next_x, next_y) not in self.simulated_blocks:
                        simu_g = Guard2(self.position, self.array, self.direction)
                        res = simu_g.move(True, (next_x, next_y))
                        self.simulated_blocks.add((next_x, next_y))
                        if res:
                            self.found_loop_blocks.add((next_x, next_y))
                    self.position = (next_x, next_y)
                else:
                    self.position = (next_x, next_y)


part2()






