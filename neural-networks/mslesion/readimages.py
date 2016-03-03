import SimpleITK
import sys
import cv2
import os

fname = sys.argv[1]

image = SimpleITK.ReadImage(fname)
imgarray = SimpleITK.GetArrayFromImage(image)
path = 'images'

if not os.path.exists(path):
    os.mkdir(path)

for i in range(512):
    cv2.imwrite( os.path.join(path,str(i)+'.jpeg'), imgarray[i] )
