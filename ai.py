#! /usr/bin/env python3

from pymongo import MongoClient
from PIL import Image
from tools import getColor
import argparse

class branchItem:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.pixels = self.image.load()
    
    def createBlocks(self, nbr):
        for i in range(nbr):
            img = Image.open(self.path)
            px = img.load()
            maxX, maxY = img.size
            lock = False
            inBlock = False
            save = -1
            for y in range(maxY):
                for x in range(maxX):
                    if getColor(px[x, y]) == "Green" or getColor(px[x, y]) == "Yellow":
                        lock = True
                        if not(inBlock):
                            inBlock = True
                            save += 1
                        if save == i:
                            if getColor(px[x - 1, y]) != "Green" and getColor(px[x - 1, y]) != "Yellow":
                                px[x - 1, y] = (0, 0, 0, 0)
                            if getColor(px[x + 1, y]) != "Green" and getColor(px[x + 1, y]) != "Yellow":
                                px[x + 1, y] = (0, 0, 0, 0)
                            if getColor(px[x, y - 1]) != "Green" and getColor(px[x, y - 1]) != "Yellow":
                                px[x, y - 1] = (0, 0, 0, 0)
                            if getColor(px[x, y + 1]) != "Green" and getColor(px[x, y + 1]) != "Yellow":
                                px[x, y + 1] = (0, 0, 0, 0)
                            if getColor(px[x - 1, y - 1]) != "Green" and getColor(px[x - 1, y - 1]) != "Yellow":
                                px[x - 1, y - 1] = (0, 0, 0, 0)
                            if getColor(px[x + 1, y + 1]) != "Green" and getColor(px[x + 1, y + 1]) != "Yellow":
                                px[x + 1, y + 1] = (0, 0, 0, 0)
                            if getColor(px[x - 1, y + 1]) != "Green" and getColor(px[x - 1, y + 1]) != "Yellow":
                                px[x - 1, y + 1] = (0, 0, 0, 0)
                            if getColor(px[x + 1, y - 1]) != "Green" and getColor(px[x + 1, y - 1]) != "Yellow":
                                px[x + 1, y - 1] = (0, 0, 0, 0)
                if not(lock):
                    inBlock = False
                lock = False
            for y in range(maxY):
                for x in range(maxX):
                    if px[x, y] == (0, 0, 0, 0):
                        px[x, y] = (255, 0, 0, 255)
            img.save("Part" + str(i + 1) + ".png")
    
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
        self.createBlocks(len(blocks))
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
                im = Image.open("Part" + str(id + 1) + ".png")
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

def testmain(args):
    link = "mongodb+srv://Flylens:Eip2024@cluster0.1v9gy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    filepath = "sample.png"
    if args.dbLink:
        link = args.dbLink
    if args.password:
        password = input("Type in the database password: ")
        toFind = "<password>"
        save = link.find(toFind)
        link = link[0:save] + password + link[save + len(toFind):len(link)]
        # mongodb+srv://Flylens:<password>@cluster0.1v9gy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority
    if args.upload:
        filepath = args.upload
    # link = "mongodb+srv://Flylens:Eip2024@cluster0.ffuat.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    data = loadData(filepath)
    if args.reset:
        uploadData(link, data, True)
    uploadData(link, data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--dbLink", type=str, help="the database link default is \"mongodb+srv://Flylens:Eip2024@cluster0.1v9gy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority\"")
    parser.add_argument("-p", "--password", action="store_true", help="this option is if the password isn't in the sdLink (a read(0) will be provided)")
    parser.add_argument("-u", "--upload", type=str, help="load and upload data from the filepath of a picture")
    parser.add_argument("-r", "--reset", action="store_true", help="this option make a big clean of the collection before the push of the new informations")
    testmain(parser.parse_args())