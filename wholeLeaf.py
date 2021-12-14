#! /usr/bin/env python3

from PIL import Image
from tools import getColor

class branchItem:
    def __init__(self, path : str):
        self.path = path
        self.image = Image.open(path)
        self.pixels = self.image.load()
    
    def getStats(self):
        x, y = 0, 0
        maxX, maxY = self.image.size
        lock, inLock = False, False
        block = [()]
        blocks = [[()]]
        nbr = 0
        bigBool = False
        block.clear()
        blocks.clear()
        for y in range(maxY):
            for x in range(maxX):
                if getColor(self.pixels[x, y]) == "Green" or getColor(self.pixels[x, y]) == "Yellow":
                    inLock = True
                    bigBool = True
                    block.append(self.pixels[x, y])
            if inLock:
                lock = True
            elif lock:
                lock = False
                blocks.append(block.copy())
                block.clear()
                nbr += 1
            inLock = False
        length = 0
        result = [(1, 1, 1)]
        result.clear()
        if len(blocks) == 0 and bigBool:
            blocks.append(block.copy())
        for id in range(len(blocks)):
            length = len(blocks[id]) + 2
            if length % 2 != 0:
                length += 1
            GCount, YCount = 0, 0
            for blk in blocks[id]:
                if getColor(blk) == "Green":
                    GCount += 1
                elif getColor(blk) == "Yellow":
                    YCount += 1
            totalSize = GCount + YCount
            if totalSize != 0:
                gInt = int(GCount * 100 / totalSize * 100)
                yInt = int(YCount * 100 / totalSize * 100)
                if gInt + yInt < 10000:
                    yInt = yInt + (10000 - (gInt + yInt))
                result.append((id + 1, gInt / 100, yInt / 100))
        return result

champ = branchItem("moreRealSample.jpeg")
status = champ.getStats()
for id, green, yellow in status:
    print("id:", id, "Green:", green, "% yellow", yellow, "%", sep=' ')