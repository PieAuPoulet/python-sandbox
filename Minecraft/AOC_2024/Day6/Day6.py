from mcpi import entity
from mcpi.minecraft import Minecraft
from mcpi.block import *
import time
from mcpi.event import ChatEvent

serverAddress = "127.0.0.1"  # change to your minecraft server
pythonApiPort = 4711  # default port for RaspberryJuice plugin is 4711, it could be changed in plugins\RaspberryJuice\config.yml

mc = Minecraft.create(serverAddress, pythonApiPort)



def main():

    #playerPos = mc.player.getTilePos()

    mc.player.setTilePos(4, 7, 12)

    time.sleep(4)

    show_map()
    part1()

def show_map():
    puzzle_input_file = open("day6_input_full.txt", "r")

    array = []

    y = 0
    max_y = 0
    max_x = 0
    start_position = ()
    for line in puzzle_input_file:
        line = line.replace('\n', '')
        array.append([])
        for x in range(0, len(line)):
            array[y].append(line[x])
            mc.setBlock(x, 0, y, SNOW)
            mc.setBlock(x, 1, y, AIR)
            mc.setBlock(x, -1, y, SNOW_BLOCK)
            #mc.setBlock(x, -1, y, block.SNOW)
            if line[x] == '^':
                start_position = (x, y)
                mc.setBlock(x, 0, y, Block(WOOL.id, 13))
            elif line[x] == '#':
                mc.setBlock(x, 0, y, GOLD_BLOCK)
            if x > max_x:
                max_x = x
        y = y + 1
        if y > max_y:
            max_y = y


    for xx in range(-1, max_x+2):
        mc.setBlock(xx, 0, max_y, STONE)
        mc.setBlock(xx, 0, -1, STONE)
    for yy in range(-1, max_y):
        mc.setBlock(max_x + 1, 0, yy, STONE)
        mc.setBlock(-1, 0, yy, STONE)

def part1():

    puzzle_input_file = open("day6_input_full.txt", "r")

    array = []

    y = 0
    x = 0
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
    #g = Guard2(start_position, array, (0, -1))
    #g.move(False, ())
    g = Guard(start_position, array)
    g.move()
    #print(len(g.visited_positions))

class Guard:

    visited_positions = set()
    direction = (0, -1) # (x,y) vector
    position = ()

    def __init__(self, position, array):
        self.position = position
        self.array = array
        #self.entity = mc.spawnEntity(self.position[0], 0, self.position[1], entity.VILLAGER)

    def move(self):
        #print(self.position)
        while True:
            self.visited_positions.add(self.position)

            #mc.removeEntity(self.entity)
            #mc.removeEntities(entity.VILLAGER)
            #self.entity = mc.spawnEntity(self.position[0], 0, self.position[1], entity.VILLAGER)
            #time.sleep(0.2)
            next_y = self.position[1] + self.direction[1]
            next_x = self.position[0] + self.direction[0]
            if next_y < 0 or next_y >= len(self.array) or next_x < 0 or next_x >= len(self.array[0]):
                mc.setBlock(self.position[0], 0, self.position[1], LAPIS_LAZULI_BLOCK)
                return
            next_square = self.array[next_y][next_x]
            if next_square == '#':
                mc.setBlock(next_x, 0, next_y, Block(WOOL.id, 14))
                x2 = -self.direction[1]
                y2 = self.direction[0]
                self.direction = (x2, y2)
            else:
                mc.setBlock(self.position[0], 0, self.position[1], LAPIS_LAZULI_BLOCK)
                time.sleep(0.02)
                #mc.setBlock(self.position[0], 0, self.position[1], block.AIR)
                mc.setBlock(self.position[0], 0, self.position[1], ICE)
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
                        mc.setBlock(next_x, 0, next_y, BEDROCK)
                        res = simu_g.move(True, (next_x, next_y))
                        self.simulated_blocks.add((next_x, next_y))
                        if res:
                            mc.setBlock(next_x, 1, next_y, COBBLESTONE)
                            self.found_loop_blocks.add((next_x, next_y))
                    mc.setBlock(self.position[0], 0, self.position[1], ICE)
                    #time.sleep(0.01)
                    mc.setBlock(self.position[0], 0, self.position[1], AIR)
                    self.position = (next_x, next_y)
                else:
                    mc.setBlock(self.position[0], 0, self.position[1], LAPIS_LAZULI_BLOCK)
                    #time.sleep(0.01)
                    mc.setBlock(self.position[0], 0, self.position[1], AIR)
                    self.position = (next_x, next_y)

while True:
    for event in mc.events.pollChatPosts():
        if "top" in event.message:
            mc.postToChat("Ok")
            show_map()
            part1()
        if "go" in event.message:
            mc.postToChat("Ok")
            part1()
        if "map" in event.message:
            mc.postToChat("Ok")
            show_map()
        if "tp" in event.message:
            mc.postToChat("Ok")
            mc.player.setTilePos(4, 7, 12)

#main()


