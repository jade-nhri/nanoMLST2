#!/usr/bin/env python3
import os,sys
import subprocess
import pandas as pd
import numpy as np

mydirs=[x for x in os.listdir() if os.path.isdir(x) if 'barcode' in x]
#print (mydirs)

LSD=[]
for i in sorted (mydirs):
#for i in ['barcode82']:
    if not os.path.exists(i+'.fastq.gz'):
        comm='cat {0}/*.fastq.gz > {0}.fastq.gz'.format(i)
        #print (comm)
        subprocess.getoutput(comm)
       
    comm='minimap2 /opt/nanoMLST2/SA_PCR-fullength.fa {0}.fastq.gz > {0}.paf'.format(i)
    #print (comm)
    subprocess.getoutput(comm)


    df=pd.read_table(i+'.paf',names=['Qname','Qlen','Qstart','Qend','strand','Tname','Tlen','Tstart','Tend','Nmatch','Alen','MQ1','MQ2','MQ3','MQ4','MQ5','MQ6','MQ7'],sep='\t') 
    #print (df)
 
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



