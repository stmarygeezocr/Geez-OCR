#!/usr/bin/env python2
import sys
import cv2
import numpy as np

"""
	left click drag an unconstrained rectangle
	press <space> once to save and next
	press <c> to clear selection rectangle
	if <space> is pressed without the rectangle, just go to the next image
"""

sx, sy = -1, -1
img_path = sys.argv[1]

def dr(event, x, y, flags, param):                              
    global sx, sy, img
    im = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
            sx, sy = x, y
            print "Mouse Down: ", sx, sy
    if sx != -1 and event == cv2.EVENT_LBUTTONUP:
            cim = img[sy:y, sx:x]
            cv2.imshow("cropped", cim)
            r = cv2.waitKey(0)
            if r == ord('c'):
               cv2.destroyWindow("cropped")
            elif r == 32:
               cv2.imwrite(img_path, cim)
               #cv2.destroyAllWindows()
               cv2.destroyWindow("cropped")
            sx, sy = -1, -1
    if sx != -1 and event == cv2.EVENT_MOUSEMOVE:
            cv2.rectangle(im, (sx, sy), (x, y), (0, 255, 0), 1)
            cv2.imshow("image", im)
            if cv2.waitKey(1) == ord('c'):
					sx, sy = -1



img = cv2.imread(img_path)
cv2.namedWindow("image")
cv2.setMouseCallback("image", dr)
cv2.imshow("image", img)
while True:
	if cv2.waitKey(1) == ord('q'):
		break
	
