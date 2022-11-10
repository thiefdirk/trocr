#-*- coding: utf-8 -*-
path = 'D:\study_data\_data\deep-text-recognition-benchmark\data/'

# import gt_train, gt_validation and replace /t with ,
# and erase the train/, validation/ part

# import gt_train, gt_validation and replace /t with ,
# and erase the train/, validation/ part
import pandas as pd
import os
import shutil

#import txt file


# cp949 encoding

gt_train = pd.read_csv(path + 'gt_train.txt',  header = None, encoding='cp949')
gt_validation = pd.read_csv(path + 'gt_validation.txt',  header = None, encoding='cp949')


# gt_train = pd.read_csv(path + 'gt_train.txt', sep=',', header=None)
# gt_validation = pd.read_csv(path + 'gt_validation.txt', sep=',', header=None)

# separate image name and label by /t

gt_train = gt_train[0].str.split('\t', expand=True)
gt_validation = gt_validation[0].str.split('\t', expand=True)

gt_train.columns = ['image', 'label']
gt_validation.columns = ['image', 'label']

# erase the train/, validation/ from image column

gt_train['image'] = gt_train['image'].apply(lambda x: x.split('/')[-1])
gt_validation['image'] = gt_validation['image'].apply(lambda x: x.split('/')[-1])

print(gt_train.head())
print(gt_validation.head())


#concatenate gt_train and gt_validation

gt = pd.concat([gt_train, gt_validation], axis=0)

print(gt.head())
print(len(gt))

# remove columns name from gt
# save as utf-8 encoding


gt.to_csv(path + 'labels.csv', header=False, index=False, encoding='utf-8')






