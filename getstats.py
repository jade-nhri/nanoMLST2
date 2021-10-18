#!/usr/bin/env python3
import os,sys
import pandas as pd
import numpy as np

infile='stats.txt'


df=pd.read_table(infile,skiprows=[0], names=['file','format',  'type','num_seqs', 'sum_len',  'min_len',  'avg_len' ,'max_len'],sep='\s+')
print (df)

filenames=df['file'].values
filecounts=df['num_seqs'].values
#print (filenames)

bcs=[]
for i in filenames:
    bc=i.split('/')[0]
    #print (bc)
    if bc not in bcs:
        bcs.append(bc)
print (bcs)

bccounts=dict()
for k in bcs:
    count=0
    for i,j in zip(filenames,filecounts):
        j=int(j.replace(',',''))
        if k in i:
            #print ('{0}\t{1}'.format(i,j))
            count+=j
        bccounts[k]=count
#print (bccounts)

for i in bccounts.keys():
    print ('{0}\t{1}'.format(i,bccounts[i]))
