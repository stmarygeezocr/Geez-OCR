#!/usr/bin/env python
import sys
import os

import csv

from sklearn.neural_network import MLPClassifier
import numpy as np
import cv2

"""
	./train.py training.csv testing.csv
"""

tr_file = sys.argv[1]
ts_file = sys.argv[2]

lbl_csv = csv.reader(open("labeles.csv", "r"))
let_num = {}
lets = lbl_csv.next()
i = 0
for l in lets:
    let_num[l] = i
	i += 1

tr_csv = csv.reader(open(tr_file, "r"))
ts_csv = csv.reader(open(ts_file, "r"))

tr_y = [let_num[i] for i in tr_csv.next()]
tr_x = []
for i in tr_csv:
	tr_x.append(i)

tr_x = np.transpose(tr_x)
tr_x = np.array(tr_x, np.uint8)

clf = MLPClassifier(activation='logistic', solver='sgd', alpha=1e-5,
hidden_layer_sizes=(864, 570), random_state=1, early_stopping=True,
validation_fraction=0.1)
clf.fit(tr_x.tolist(), tr_y)

import pickle
s = pickle.dump(clf, open("model6.dump", "w"))

ts_y = [let_num[i] for i in ts_csv.next()]
ts_x = []
for i in ts_csv:
	ts_x.append(i)
ts_x = np.transpose(ts_x)
ts_x = np.array(ts_x, np.uint8)

TPR = 0
TNR = 0
PPV = 0
NPV = 0
FNR = 0
FPR = 0
FDR = 0
FOR = 0
ACC = 0
TP = 0
FP = 0
TN = 0
FN = 0
for i in range(len(ts_y)):
	r = clf.predict([ts_x[i]])
	if r[0] == ts_y[i]:
		TP += 1
print "accuracy:", float(TP)/len(ts_y) * 100.0



















