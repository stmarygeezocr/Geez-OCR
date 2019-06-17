#!/usr/bin/env python2
from sklearn.neural_network import MLPClassifier
import csv
import sys
import cv2
import numpy as np
import pickle

"""
	./run.py model label image
"""

model_path = sys.argv[1]
label_path = sys.argv[2]
img_path = sys.argv[3]



lbl_csv = csv.reader(open(label_path, "r"))
let_num = {}
lets = lbl_csv.next()
i = 0
for l in lets:
   let_num[l] = i
   i += 1

def get_let_name(code):
	for i, j in let_num.iteritems():
		if j == code:
			return i

clf = pickle.load(open(model_path, "r"))
img = cv2.imread(img_path)
h, w = img.shape[:2]
img = cv2.resize(img, (int(w * 2), int(h * 2)), cv2.INTER_CUBIC)
img2 = img.copy()
gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray image", gimg)
_, thr = cv2.threshold(gimg, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("binary image", thr)
kernel = np.ones((5,5), np.uint8)
dimg = cv2.dilate(thr, kernel, iterations=4)
cv2.imshow("dilated image", dimg)
eimg = cv2.Canny(dimg, 50, 150, apertureSize=5)
cv2.imshow("edges image", eimg)
lines = cv2.HoughLines(eimg, 1, np.pi/180, 100)
tavg = 0
n = 0
ly1y2 = []
for line in lines:
   for rho, theta in line:
      a = np.cos(theta);b = np.sin(theta)
      x0 = a * rho;y0 = b * rho
      x1 = int(x0 + 1000*(-b))
      y1 = int(y0 + 1000*(a))
      x2 = int(x0 - 1000*(-b))
      y2 = int(y0 - 1000*(a))
      color = (0, 0, 255)
      if (y2 - y1) < (x2 - x1):
          color = (0, 255, 0)
          if int(theta) != 0:
              tavg += theta
              n += 1
      cv2.line(img, (x1, y1), (x2, y2), color, 2)
      cv2.line(img2, (x1, y1), (x2, y2), color, 2)
      print "X1, Y1: ", x1, y1, "x2,y2: ", x2, y2
      ly1y2.append(y1 > y2)

tavg = tavg / n
print tavg
r, c, _ = img.shape
M = cv2.getRotationMatrix2D((c/2, r/2), np.degrees(tavg) -90, 1)
img2 = cv2.warpAffine(img2, M, (c, r))
final = cv2.warpAffine(thr, M, (c, r))
cv2.imshow("final", final)
kernel = np.ones((3, 3), np.uint8)
final = cv2.morphologyEx(final, cv2.MORPH_CLOSE, kernel, iterations=1)
im, conts, heir = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
conts.reverse()

cv2.imshow("original", img)
cv2.imshow("process", img2)
cv2.imshow("preprocessed", final)
cv2.imwrite("final-image.jpg", final)
cv2.waitKey(0)
i = 0
result = []
for cont in conts:
   x, y, w, h = cv2.boundingRect(cont)
   ccim = cv2.resize(final[y - int(h*0.2):y+h+int(h*0.2),x-int(w*0.2):x+w+int(w*0.2)], (34, 34))
   cim = cv2.resize(final[y - int(h*0.2):y+h+int(h*0.2),x-int(w*0.2):x+w+int(w*0.2)], (34, 34))
   cim[cim == 255] = 1
   flat_list = list(cim.flatten())
   pred = clf.predict([flat_list])
   cv2.imwrite("characters/chr-" + get_let_name(pred[0]) + ".png", ccim)
   result.append(pred[0])
   i += 1
s = ""
#for i in result:
#	s += get_let_name(i)
#print "recognition:", s
