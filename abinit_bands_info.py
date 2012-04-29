#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 28-04-2012 17:53:58
@author: Maciej Chudak

Displays some info about band structure data in an Abinit .out file, intended
to be used before extracting data with abinit_bands_to_csv script.

Might display more info in the future.
'''
from abinit_bands_to_csv import find_datasets
import argparse

parser=argparse.ArgumentParser(description='Displays some info about band '+
'structure data in an Abinit .out file, intended to be used before extracting '+
'data with abinit_bands_to_csv script.')
parser.add_argument('input_file', type=str, nargs=1,
                    help='path of the .out file')
args=parser.parse_args()

# find all the datasets
with open(args.input_file[0], "r") as inf:
    datasets=find_datasets(inf)

print(str(len(datasets))+" datasets found:")

i=0
for dataset in datasets:
    print(str(i)+") "+str(dataset[1])+" k points in "+str(dataset[0]))
    i+=1


