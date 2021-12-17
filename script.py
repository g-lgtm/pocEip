#! /usr/bin/env python3

from pymongo import MongoClient
from PIL import Image

def sendRawData(filepath, name = "allc", link = "mongodb+srv://Flylens:Eip2024@poc.1v9gy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"):
    client = MongoClient(link)
    db = client.AnalyseField
    collection = db.raws
    im = Image.open(filepath)
    x, y = im.size
    collection.delete_one({"name": name})
    collection.insert_one({"name": name, "sizex": x, "sizey": y, "png": im.tobytes()})