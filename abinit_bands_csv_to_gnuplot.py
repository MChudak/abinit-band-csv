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
from itertools import permutations

# most basic k_label k points
basic_critical_k={
    "FCC":{"Γ":{(0.0, 0.0, 0.0)},
           "X":{(1/2, 1/2, 0.0)},
           "L":{(1/2, 0.0, 0.0), (1/2, 1/2, 1/2)},
           "K":{(3/4, 3/8, 3/8), (3/8, 0.0,-3/8)},
           "U":{(5/8, 1/4, 1/4), (5/8, 3/8, 0.0), (3/8, 3/8,-1/2)},
           "W":{(3/4, 1/2, 1/4), (1/2, 1/4,-1/4)}}}

# generating all possible coordinates of the basic k_label k points
all_critical_k=dict()
# for every structure (SC, BCC, FCC, etc.)
for structure in basic_critical_k:
    all_critical_k[structure]=dict()
    # for every k_label point ('G'. 'X', 'L', etc.)
    for point in basic_critical_k[structure]:
        all_critical_k[structure][point]=set()
        # for each basic k_label k point coordinate 
        for basic_k in basic_critical_k[structure][point]:
            for k in permutations(basic_k):
                all_critical_k[structure][point].add(tuple(k))
                all_critical_k[structure][point].add(tuple(map(lambda x:-x, k)))


def print_k_dict(k_dict):
    # print possible points
    for structure in sorted(k_dict):
        print(structure+":")
        for point in sorted(k_dict[structure]):
            print("->  "+point+":")
            i = 1
            for k in sorted(k_dict[structure][point]):
                print(" ",i,"\t",k)
                i+=1


def label_k_point(k_point, k_dict):
        k=list()
        # move all coords to the first Brillouin zone
        for ki in k_point:
            if round(ki)==ki: k.append(0.0)
            else: k.append((ki+1)%2-1)
        k=tuple(k)

        for critical_k in k_dict:
            if k in k_dict[critical_k]:
                return critical_k # the point is k_label
        
        return None # only if the point is not k_label


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

# find characteristic high symmetry (k_label) points
i=1
for line in lines[3:]:
    nums=re.findall(regexps['value'], line)[:4]
    k_label=label_k_point(tuple(map(lambda x:float(x), nums[1:4])), all_critical_k["FCC"])
    if k_label is not None:
        print("set xtics add ('"+k_label+"' "+str(i)+")")
    i+=1

print('''
plot    ''', end='')

for i in range(num_of_bands):
    if i>0: print("        ", end='')
    print("'"+args.csv_file[0]+"' using 1:"+str(i+5)+" notitle w l lt -1", end='')
    if i+1<num_of_bands: print(",\\")
    else: print()








