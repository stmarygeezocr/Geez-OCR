#!/usr/bin/env python2
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import csv
import sys
import numpy as np
import pickle

"""
  ./test.py test.csv model
"""

lbl_csv = csv.reader(open("label.csv", "r"))
let_num = {}
for l in lbl_csv:
   let_num[l[0].replace(" ", "")] = int(l[1])
   print l[0].replace(" ", "") + "," + l[1]


def get_let_name(code):
   for i, j in let_num.iteritems():
      if j == code:
         return i


ts_csv = csv.reader(open(sys.argv[1], "r"))
ts_y  = ts_csv.next()
ts_y = [let_num[i] for i  in ts_y]
ts_x = []
for i in ts_csv:
   ts_x.append(i)

ts_x = np.transpose(ts_x)
ts_x = np.array(ts_x, np.uint8)

clf = pickle.load(open(sys.argv[2], "r"))
TP = 0
res = {}
pred_y = []
for l in let_num.keys():
    res[l] = {'TP' : 0, 'FP' : 0,
              'TN' : 0, 'FN' : 0}
for i in range(len(ts_y)):
    r = clf.predict([ts_x[i]])
    pred_y.append(r[0])
    if r[0] == ts_y[i]:
        res[get_let_name(ts_y[i])]['TP'] += 1
        TP += 1
        for l in let_num.keys():
            if l != get_let_name(ts_y[i]):
                res[l]['TN'] += 1
    else:
        res[get_let_name(r[0])]['FP'] += 1
        res[get_let_name(ts_y[i])]['FN'] += 1

n = len(ts_y)
print "Letter,TP,TN,FP,FN,Accuracy,Precision,Recall,F1"
for let, resv in res.iteritems():
    acc = ((float(resv['TP']) + float(resv['TN'])) / len(ts_y)) * 100.0
    tpfp = (float(resv['TP']) + float(resv['FP']))
    pre = (0 if tpfp == 0 else (float(resv['TP']) / tpfp)) * 100 
    tpfn = (float(resv['TP']) + float(resv['FN']))
    rec = (0 if tpfn == 0 else (float(resv['TP']) / tpfn)) * 100
    ppr = pre + rec
    f1 = (0 if ppr == 0 else (2 * ((pre * rec) / ppr)))
    print let, ",", resv['TP'], ",", resv['TN'], ",", resv['FP'], ",", resv['FN'], ",", acc, ",", pre, ",", rec, ",", f1

print "accuracy:", float(TP)/len(ts_y) * 100.0

# sklearn metrics
print "** sklearn metrics **"
print "TP: ", TP, "  LEN_Y: ", len(ts_y)
print "Accuracy: ", accuracy_score(ts_y, pred_y)
