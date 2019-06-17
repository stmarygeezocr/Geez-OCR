#!/usr/bin/env python2

import cv2
import numpy as np

import sys
import os

def largest_contour(conts):
	largest_cont = []
	max_area = 0
	for cont in conts:
		if max_area < cv2.contourArea(cont):
			max_area = cv2.contourArea(cont)
			largest_cont = cont
	return largest_cont

files = os.listdir(sys.argv[1])

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
for f in files:
	img = cv2.imread(sys.argv[1]+"/"+f)
	h, w = np.shape(img)[:2]
	if h > w + (0.9 * w):
		print sys.argv[1]+"/"+f
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
"""
os.mkdir(sys.argv[1]+"seged")
for f in files:
	img = cv2.imread(sys.argv[1]+"/"+f)
	_, thr = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 210, 255, cv2.THRESH_BINARY_INV)
	im, conts, heir = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	x, y, w, h = cv2.boundingRect(largest_contour(conts))
	cv2.imwrite(sys.argv[1]+"seged/"+ f, img[y:y+h, x:x+w])
"""
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
