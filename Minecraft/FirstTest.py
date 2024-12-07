from mcpi.minecraft import Minecraft
import mcpi.block as block
from math import *

serverAddress="127.0.0.1" # change to your minecraft server
pythonApiPort=4711 #default port for RaspberryJuice plugin is 4711, it could be changed in plugins\RaspberryJuice\config.yml

mc = Minecraft.create(serverAddress,pythonApiPort)
pos = mc.player.getPos()

print("pos: x:{},y:{},z:{}".format(pos.x,pos.y,pos.z))

playerPos = mc.player.getTilePos()
colors = [14, 1, 4, 5, 3, 11, 10]
height = 50

for x in range(0, 128):
    for colourindex in range(0, len(colors)):
        y = playerPos.y + sin((x / 128.0) * pi) * height + colourindex
        mc.setBlock(playerPos.x + x - 64, int(y), playerPos.z, block.WOOL.id, colors[len(colors) - 1 - colourindex])
print("rainbow created at x:{} y:{} z:{}".format(playerPos.x, playerPos.y, playerPos.z))
