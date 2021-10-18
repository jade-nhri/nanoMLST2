#!/usr/bin/env python3
import os,sys
import subprocess
import multiprocessing as mp
import time 
from time import sleep 

indir=sys.argv[1]
indir=os.path.abspath(indir)
print (indir)
outdir=sys.argv[2]
threads=int(sys.argv[3])

if not os.path.exists(outdir):
    os.mkdir(outdir)

def run(qfile,name,outdir):
    comm='medaka_consensus -i {0} -d /opt/nanoMLST2/SA_PCR-fullength.fa -o {2}/{1}'.format(qfile,name,outdir)
    print (comm)
    subprocess.getoutput(comm)

def main():
    po=mp.Pool(16)
    for i in sorted(myfiles):
        qfile=os.path.join(indir,i)
        name=i.split('.')[0]
        if os.path.exists(os.path.join(outdir,name)+'/consensus.fasta'):
            continue
        po.apply_async(run,[qfile,name,outdir])
    po.close()
    po.join()


myfiles=[x for x in os.listdir(indir) if 'fastq.gz' in x]
N=len(myfiles)
print (N)
if __name__=='__main__':
    po=mp.Pool(threads)
    for i in sorted(myfiles):
        qfile=os.path.join(indir,i)
        name=i.split('.')[0]
        if os.path.exists(os.path.join(outdir,name)+'/consensus.fasta'):
            continue
        po.apply_async(run,[qfile,name,outdir])
    po.close()
    po.join()

for i in range(0,5):
    if __name__=='__main__':
        main()
    comm='ls {0}/*/consensus.fasta | wc -l'.format(outdir)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    countN=int(stdout)
    print (countN)
    if countN==N:
        break

for i in sorted(myfiles):
    qfile=os.path.join(indir,i)
    name=i.split('.')[0]
    comm='/opt/nanoMLST2/SA_MLSTtyping.py {1}/{0}/consensus.fasta'.format(name,outdir)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    with open (os.path.join(outdir,'log.txt') ,'a') as log:
        log.write(i+'\n'+stdout+'\n')
    with open (os.path.join(outdir,'SA_MLST_types.txt'), 'a') as types:
        lines=stdout.splitlines()
        types.write(i+'\t'+lines[-1]+'\n')

