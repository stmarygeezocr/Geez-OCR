#!/usr/bin/env python

import cv2
import numpy as np
import random

f = open("geez-characters.txt", "r")
l = f.readlines()
ls = [i.replace("\n", "") for i in l]

img = np.ones((842, 595, 3), np.uint8) * 255 # 72 DPI
#img = np.ones((3508, 2480, 3), np.uint8) * 255 # 300 DPI

ft = cv2.freetype.createFreeType2()
ft.loadFontData(fontFileName="abyssinia.ttf", id=0)

for lt in ls:
	x = int(img.shape[1] * 0.05)
	y = int(img.shape[0] * 0.05)
	#img = np.ones((842, 595, 3), np.uint8) * 255 # 72 DPI
	img = np.ones((3508, 2480, 3), np.uint8) * 255 # 300 DPI
	i = 0
	while y < int(img.shape[0] - img.shape[0]*0.01):
		size = random.randint(15, 30)
		b, g, r = random.randrange(150), random.randrange(150), random.randrange(150)
		img = ft.putText(img, lt, (x, y), size, (b, g, r), -2, cv2.LINE_AA, True)
		x += int(size + size * 0.4)
		if x > (img.shape[1] - img.shape[1]*0.05):
			x = int(img.shape[1] * 0.05)
			y += int(size + size * 0.25)
		i += 1
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite("generated/" + lt + ".png", img)
	print "Character:", lt, " -- Count:", i
