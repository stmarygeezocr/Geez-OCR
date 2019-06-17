#!/usr/bin/env python

import os
import sys
import csv
import cv2
import numpy as np

"""
	./dataset_prep.py dataset_dir target_dir train_pct valid_pct test_pct [to_csv]
"""

"""
dataset_dir = ""
target_dir = ""
train_pct = 0.0
valid_pct = 0.0
test_pct = 0.0
train_dir = target_dir + "/training"
valid_dir = target_dir + "/validation"
test_dir = target_dir + "/test"
to_csv = False"""
	
print "./dataset_prep.py dataset_dir target_dir train_pct valid_pct test_pct [to_csv] "
print "Options: "
print "    dataset_dir    path to folder containing original dataset"
print "    target_dir     path to folder where new dataset will be stored"
print "    train_pct      percentage of data to be used for training"
print "    valid_pct      percentage of data to be used for validation"
print "    test_pct       percentage of data to be used for testing"
print "    to_csv         (optional) set to 1 to create the new dataset as a csv file"

dataset_dir = sys.argv[1]
target_dir = sys.argv[2]
train_pct = float(sys.argv[3])
valid_pct = float(sys.argv[4])
test_pct = float(sys.argv[5])
train_dir = target_dir + "/training"
valid_dir = target_dir + "/validation"
test_dir = target_dir + "/test"
to_csv = True if sys.argv[6] == "1" else False

IMG_HEIGHT = 34
IMG_WIDTH = 34
PIXEL_SIZE = IMG_HEIGHT * IMG_WIDTH

def count_data():
	count = []
	data = os.listdir(dataset_dir)
	no_letters = len(data)
	for d in data:
		count.append(len(os.listdir(dataset_dir + "/" + d)))
	count.sort()
	return no_letters, count[0]

def img_flatten(img_path):
	return list(cv2.threshold(
		cv2.cvtColor(
			cv2.resize(
				cv2.imread(img_path),
				(34, 34),
				interpolation=cv2.INTER_LINEAR),
			cv2.COLOR_BGR2GRAY),
		127, 1, cv2.THRESH_BINARY_INV)[1].flatten())

def create_new_ds((no_letters, data_count)):
	if os.listdir(".").count(target_dir) == 0:
		os.mkdir(target_dir)
		os.mkdir(train_dir)
		os.mkdir(valid_dir)
		os.mkdir(test_dir)
		dataset = os.listdir(dataset_dir)
		for data in dataset: # iterate on letters
			dt = os.listdir(dataset_dir + "/" + data)
			os.mkdir(train_dir + "/" + data)
			os.mkdir(valid_dir + "/" + data)
			os.mkdir(test_dir + "/" + data)
			train_size = int(data_count * (train_pct / 100))
			valid_size = int(data_count * (valid_pct / 100))
			test_size = int(data_count * (test_pct / 100))
			trdata = dt[0:train_size]
			vldata = dt[train_size:train_size+valid_size]
			tsdata = dt[train_size+valid_size:train_size+valid_size+test_size]
			i = 0
			for d in trdata:
				save_path = train_dir + "/" + data + "/" + str(i) + ".png"
				fetch_path = dataset_dir + "/" + data + "/" + d
				os.system("cp " + fetch_path + " " + save_path)
				i += 1
			i = 0
			for d in vldata:
				save_path = valid_dir + "/" + data + "/" + str(i) + ".png"
				fetch_path = dataset_dir + "/" + data + "/" + d
				os.system("cp " + fetch_path + " " + save_path)
				i += 1
			i = 0
			for d in tsdata:
				save_path = test_dir + "/" + data + "/" + str(i) + ".png"
				fetch_path = dataset_dir + "/" + data + "/" + d
				os.system("cp " + fetch_path + " " + save_path)
				i += 1

def create_csv((no_letters, data_count)):
	print data_count
	if os.listdir(".").count(target_dir) == 0:
		os.mkdir(target_dir)
		dataset = os.listdir(dataset_dir)
		training_csv = target_dir + "/training.csv"
		validation_csv = target_dir + "/validataion.csv"
		testing_csv = target_dir + "/testing.csv"
		train_size = int(data_count * (train_pct / 100))
		valid_size = int(data_count * (valid_pct / 100))
		test_size = int(data_count * (test_pct / 100))
		trcsvw = csv.writer(open(training_csv, "w"))
		vlcsvw = csv.writer(open(validation_csv, "w"))
		tscsvw = csv.writer(open(testing_csv, "w"))
		tr_data_all = np.zeros((PIXEL_SIZE + 1, no_letters * train_size), dtype='O')
		ts_data_all = np.zeros((PIXEL_SIZE + 1, no_letters * test_size), dtype='O')
		vl_data_all = np.zeros((PIXEL_SIZE + 1, no_letters * valid_size), dtype='O')
		tr_label_all = []
		vl_label_all = []
		ts_label_all = []
		tr_idx = 0
		vl_idx = 0
		ts_idx = 0
		for data in dataset:
			dt = os.listdir(dataset_dir + "/" + data)
			trdata = dt[:train_size]
			vldata = dt[train_size:train_size+valid_size]
			tsdata = dt[train_size+valid_size:train_size+valid_size+test_size]
			data2write = []
			label = []
			for tr in trdata:
				fetch_path = dataset_dir + "/" + data + "/" + tr
				tr_data_all[1:,tr_idx] = img_flatten(fetch_path)
				tr_label_all.append(data)
				tr_idx += 1
			for vl in vldata:
				fetch_path = dataset_dir + "/" + data + "/" + vl
				vl_data_all[1:,vl_idx] = img_flatten(fetch_path)
				vl_label_all.append(data)
				vl_idx += 1
			for ts in tsdata:
				fetch_path = dataset_dir + "/" + data + "/" + tr
				ts_data_all[1:,ts_idx] = img_flatten(fetch_path)
				ts_label_all.append(data)
				ts_idx += 1
		tr_data_all[0,:] = tr_label_all
		vl_data_all[0,:] = vl_label_all
		ts_data_all[0,:] = ts_label_all
		np.random.shuffle(tr_data_all.transpose())
		np.random.shuffle(vl_data_all.transpose())
		np.random.shuffle(ts_data_all.transpose())
		trcsvw.writerows(tr_data_all)
		vlcsvw.writerows(vl_data_all)
		tscsvw.writerows(ts_data_all)


if to_csv:
	create_csv(count_data())
else:
	create_new_ds(count_data())
