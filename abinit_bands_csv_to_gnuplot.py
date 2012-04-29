#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 28-04-2012 18:32:12
@author: Maciej Chudak

Creates a gnuplot script that will use a csv file containing band structure
data in the following format:
path length, kx, ky, kz, one or more band energy values
Such an input file might be generated using the abinit_bands_to_csv script.

Generated output is meant to be used as a template by users that know gnuplot's
syntax. This script writes to stdout.
'''
import argparse, re
from math import floor, ceil

parser=argparse.ArgumentParser(description='''Generates a gnuplot script that \
will use a csv file containing band structure data. Writes to stdout.''')
parser.add_argument('csv_file', type=str, nargs=1, default=None,
                    help='path of the csv data file')
args=parser.parse_args()

regexps={"header":r"Eigenvalues \( *(\w+) *\) for nkpt= *([0-9]+) *k points.",
         "value" :r"([\-0-9\.]+)"}

with open(args.csv_file[0], "r") as inf:
    lines=inf.readlines()

# bad solution: script blindly assumes, that header data is in row 1
header=re.search(regexps["header"], lines[1])
unit=header.groups()[0]
num_of_points=header.groups()[1]

# -4 because there are 4 non-eigenvalues in each row
num_of_bands=len(re.findall(regexps['value'], lines[3]))-4

path_len=re.search(regexps['value'], lines[-1]).groups()[0]


print('''#!/usr/bin/gnuplot

set terminal pdf enhanced
set output "bands_graph.pdf"

set title "Band structure"

set ylabel "ħω(k)''', end='')
print(" / "+unit, end='')
print('''"
set xlabel "k"

set grid xtics

set xtics 0

''', end='')
print("set xrange [0:"+str(path_len)+"]")
print("set autoscale y\n")

# find characteristic high symmetry (critical) points
for line in lines[3:]:
    nums=re.findall(regexps['value'], line)[:4]
    
    # move all coords to the first Brillouin zone
    for i in range(1,4):
        nums[i] = float(nums[i])
        if nums[i]>= 1.0: nums[i]-=floor(nums[i])
        if nums[i]<=-1.0: nums[i]-= ceil(nums[i])
    
    # check if Gamma
    if nums[1]==nums[2]==nums[3]==0.0:
        print("set xtics add ('Γ' "+str(nums[0])+")")

print('''
plot    ''', end='')

for i in range(num_of_bands):
    if i>0: print("        ", end='')
    print("'"+args.csv_file[0]+"' using 1:"+str(i+5)+" notitle w l lt -1", end='')
    if i+1<num_of_bands: print(",\\")
    else: print()








