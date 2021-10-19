#!/usr/bin/env python3
import os,sys
import subprocess
import pandas as pd
import numpy as np
import argparse

threads=8
outpath='output'
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='the path to raw_reads folder')
parser.add_argument('-o', help='an output folder (dfault output)')
parser.add_argument('-t', help='threads (default=8)')
args = parser.parse_args()

argv=sys.argv
if '-t' in argv:
    threads=argv[argv.index('-t')+1]
if '-i' in argv:
    inpath=os.path.abspath(argv[argv.index('-i')+1])
if '-o' in argv:
    outpath=argv[argv.index('-o')+1]

outpath=os.path.abspath(outpath)

if not os.path.exists(outpath):
    os.mkdir(outpath)

os.chdir(inpath)
mydirs=[x for x in os.listdir() if os.path.isdir(x) if 'barcode' in x]
#print (mydirs)

LSD=[]
for i in sorted (mydirs):
    if not os.path.exists(os.path.join(outpath,i+'.fastq.gz')):
        comm='cat {0}/*.fastq.gz > {1}/{0}.fastq.gz'.format(i,outpath)
        #print (comm)
        subprocess.getoutput(comm)
       
    comm='minimap2 /opt/nanoMLST2/SA_PCR-fullength.fa {1}/{0}.fastq.gz -t {2} > {0}.paf'.format(i,outpath,threads)
    #print (comm)
    subprocess.getoutput(comm)


    df=pd.read_table(i+'.paf',names=['Qname','Qlen','Qstart','Qend','strand','Tname','Tlen','Tstart','Tend','Nmatch','Alen','MQ1','MQ2','MQ3','MQ4','MQ5','MQ6','MQ7'],sep='\t') 
    #print (df)
    comm='rm {0}.paf'.format(i)
    subprocess.getoutput(comm)
 
    genes=np.unique(df['Tname'].values)
    #print (genes)

    gcounts=dict()
    for j in genes:
        dfset=df[df['Tname']==j]
        gcounts[j]=len(np.unique(dfset['Qname'].values))
        if gcounts[j]<40:
            if i not in LSD:
                LSD.append(i)
    print ('{0}\t{1}'.format(i,gcounts))

print (LSD)



