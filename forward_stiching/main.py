import cv2
import os

myFolders = ['images']

for folder in myFolders:
    path = folder
    images = []
    myList = os.listdir(path)

    for Img in myList:
        curImg = cv2.imread(f'{path}/{Img}')
        curImg = cv2.resize(curImg, (0,0), None, 1, 1)
        images.append(curImg)

    stitcher = cv2.Stitcher.create(mode = 1)
    (status, result) = stitcher.stitch(images)
    if (status == cv2.STITCHER_OK):
        cv2.imwrite("./result.jpg", result)
    else:
        print(status)

