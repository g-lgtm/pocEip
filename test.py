#! /usr/bin/env python3

from script import sendRawData as send

send("./moreRealSample.png", "imageTest")

# from PIL import Image

# from tools import getColor
# class blockGesture:
#     def __init__(self, path):
#         self.path = path
#         self.image = Image.open(path)
#         self.pixels = self.image.load()
#         self.imgs = {}
    
#     def createBlocks(self):
#         maxX, maxY = self.image.size
#         lock = False
#         inBlock = False
#         fEnd = True
#         block = [()]
#         blocks = [[()]]
#         block.clear()
#         blocks.clear()
#         savex, savey, saveminx, saveminy = 0, 0, 0, 0
#         maxmins = [()]
#         maxmins.clear()
#         first = True
#         for y in range(maxY):
#             for x in range(maxX):
#                 if getColor(self.pixels[x, y]) == "Green" or getColor(self.pixels[x, y]) == "Yellow":
#                     lock = True
#                     fEnd = True
#                     if not(inBlock):
#                         if first:
#                             first = False
#                         else:
#                             blocks.append(block.copy())
#                             block.clear()
#                             maxmins.append((savex - (saveminx - 1), savey - (saveminy - 1), saveminx, saveminy))
#                         savex, savey, saveminx, saveminy = 0, 0, x, y
#                         inBlock = True
#                     block.append((x, self.pixels[x, y]))
#                     if x > savex:
#                         savex = x
#                     elif x < saveminx:
#                         saveminx = x
#                     if y > savey:
#                         savey = y
#                     elif y < saveminy:
#                         saveminy = y
#                 elif inBlock and lock and fEnd:
#                     fEnd = False
#                     block.append((0, (-1, -1, -1, -1)))
#             if not(lock):
#                 inBlock = False
#             elif block[len(block) - 1] != (0, (-1, -1, -1, -1)):
#                 block.append((0, (-1, -1, -1, -1)))
#             lock = False
#         blocks.append(block.copy())
#         maxmins.append((savex - (saveminx - 1), savey - (saveminy - 1), saveminx, saveminy))
#         for i in range(len(blocks)):
#             x, y, minx, miny = maxmins[i]
#             img = Image.new('RGBA', (x + 1, y + 1), (0, 0, 0, 0))
#             tmppix = img.load()
#             tmpx, tmpy = 0, 0
#             tmpblock = blocks[i]
#             rank = 0
#             savedX, col = tmpblock[rank]
#             tmpx = savedX - minx
#             while rank < len(tmpblock):
#                 savedX, col = tmpblock[rank]
#                 if col == (-1, -1, -1, -1):
#                     rank += 1
#                     if rank >= len(tmpblock):
#                         break
#                     savedX, col = tmpblock[rank]
#                     tmpx = savedX - minx
#                     tmpy += 1
#                 else:
#                     tmpx += 1
#                 tmppix[tmpx, tmpy] = col
#                 rank += 1
#             self.imgs["Part" + str(i + 1) + ".png"] = img.copy()
#     def getSt(self):
#         self.createBlocks()
#         for img in self.imgs:
#             self.imgs[img].save(img)

# blockGesture("./sample.png").getSt()

# from pymongo import MongoClient
# client = MongoClient("mongodb+srv://Flylens:Eip2024@poc.1v9gy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# db = client.AnalyseField

# collection = db.fields
# for two in collection.find():
#     print ("name: ", two["name"], " green: ", two["green"], "% yellow: ", two["yellow"], " sizeX: ", two["sizex"], " sizeY: ", two["sizey"], sep='')
#     sizeX, sizeY = two["sizex"], two["sizey"]
#     Image.frombytes("RGBA", (sizeX, sizeY), two["png"]).show()

# push = db.raws
# toPush = {}
# toPush["name"] = "allc"
# im = Image.open("./sample.png")
# toPush["sizex"], toPush["sizey"] = im.size
# toPush["png"] = im.tobytes()
# push.insert_one(toPush)