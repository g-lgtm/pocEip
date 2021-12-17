#! /usr/bin/env python3

from pymongo import MongoClient
from PIL import Image
from tools import getColor
import signal
from time import sleep, ctime
import time

def signal_handler(sig, frame):
    print()
    print("LEAVING", end='', flush=True)
    sleep(0.2)
    print(".", end='', flush=True)
    sleep(0.8)
    print(".", end='', flush=True)
    sleep(0.8)
    print(".", flush=True)
    exit()

class branchItem:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.pixels = self.image.load()
        self.imgs = {}
    
    def createBlocks(self):
        maxX, maxY = self.image.size
        lock = False
        inBlock = False
        fEnd = True
        block = [()]
        blocks = [[()]]
        block.clear()
        blocks.clear()
        savex, savey, saveminx, saveminy = 0, 0, 0, 0
        maxmins = [()]
        maxmins.clear()
        first = True
        for y in range(maxY):
            for x in range(maxX):
                if getColor(self.pixels[x, y]) == "Green" or getColor(self.pixels[x, y]) == "Yellow":
                    lock = True
                    fEnd = True
                    if not(inBlock):
                        if first:
                            first = False
                        else:
                            blocks.append(block.copy())
                            block.clear()
                            maxmins.append((savex - (saveminx - 1), savey - (saveminy - 1), saveminx, saveminy))
                        savex, savey, saveminx, saveminy = 0, 0, x, y
                        inBlock = True
                    block.append((x, self.pixels[x, y]))
                    if x > savex:
                        savex = x
                    elif x < saveminx:
                        saveminx = x
                    if y > savey:
                        savey = y
                    elif y < saveminy:
                        saveminy = y
                elif inBlock and lock and fEnd:
                    fEnd = False
                    block.append((0, (-1, -1, -1, -1)))
            if not(lock):
                inBlock = False
            elif block[len(block) - 1] != (0, (-1, -1, -1, -1)):
                block.append((0, (-1, -1, -1, -1)))
            lock = False
        blocks.append(block.copy())
        maxmins.append((savex - (saveminx - 1), savey - (saveminy - 1), saveminx, saveminy))
        for i in range(len(blocks)):
            x, y, minx, miny = maxmins[i]
            img = Image.new('RGBA', (x + 1, y + 1), (0, 0, 0, 0))
            tmppix = img.load()
            tmpx, tmpy = 0, 0
            tmpblock = blocks[i]
            rank = 0
            savedX, col = tmpblock[rank]
            tmpx = savedX - minx
            while rank < len(tmpblock):
                savedX, col = tmpblock[rank]
                if col == (-1, -1, -1, -1):
                    rank += 1
                    if rank >= len(tmpblock):
                        break
                    savedX, col = tmpblock[rank]
                    tmpx = savedX - minx
                    tmpy += 1
                else:
                    tmpx += 1
                tmppix[tmpx, tmpy] = col
                rank += 1
            self.imgs["Part" + str(i + 1) + ".png"] = img.copy()

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
        names = []
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
                names.append("Part" + str(nbr))
            inLock = False
        length = 0
        result = [("", 1, 1, 1)]
        result.clear()
        if len(blocks) == 0 and bigBool:
            blocks.append(block.copy())
            nbr += 1
        self.createBlocks()
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
                im = self.imgs["Part" + str(id + 1) + ".png"]
                result.append((names[id], id + 1, gInt / 100, yInt / 100, im.tobytes(), im.size))
        return result

def loadData(filepath):
    champ = branchItem(filepath)
    status = champ.getStats()
    result = [{"name":"", "green":"0", "yellow":"0", "png": '/'}]
    result.clear()
    gMoy = 0.0
    yMoy = 0.0
    for name, id, green, yellow, pixels, size in status:
        gMoy += green
        yMoy += yellow
        sizeX, sizeY = size
        result.append({"name":name, "green":str(green), "yellow":str(yellow), "png": pixels, "sizex": sizeX, "sizey" : sizeY})
    gMoy /= len(result)
    yMoy /= len(result)
    gMoy = int(gMoy * 100) / 100
    yMoy = int(yMoy * 100) / 100
    if gMoy + yMoy < 100:
        yMoy += 100 - (gMoy + yMoy)
        yMoy = int(yMoy * 100) / 100
    return ((filepath, gMoy, yMoy), result)

def uploadData(link, data, reset=False):
    client = MongoClient(link)
    db = client.AnalyseField
    collection = db.fields
    other, stats = data
    filePath, gMoy, yMoy = other
    if reset:
        for doc in collection.find():
            collection.delete_one(doc)
    collection.delete_one({"name": "Part0"})
    im = Image.open(filePath)
    sizeX, sizeY = im.size
    collection.insert_one({"name": "Part0", "green": str(gMoy), "yellow": str(yMoy), "png": im.tobytes(), "sizex": sizeX, "sizey" : sizeY})
    for res in stats:
        collection.delete_one({"name":res["name"]})
        collection.insert_one(res)

def getNewInfo(db):
    collection = db.raws
    asNew = collection.find()
    for doc in asNew:
        collection.delete_one({"name": doc["name"]})
        return doc
    return None

def pushNewInfo(info):
    if info["name"] == "allc":
        Image.frombytes("RGBA", (info["sizex"], info["sizey"]), info["png"]).save(".__aicache__.png")
        uploadData("mongodb+srv://Flylens:Eip2024@poc.1v9gy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", loadData(".__aicache__.png"))
    return

def main(every):
    client = MongoClient("mongodb+srv://Flylens:Eip2024@poc.1v9gy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.AnalyseField
    while True:
        newInfo = getNewInfo(db)
        if newInfo:
            print("Got data at:", end=' ')
            print(ctime())
            pushNewInfo(newInfo)
            print("data pushed at:", end=' ')
            print(ctime())
        sleep(every)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main(3600 / 2)