#!/usr/bin/env python3
import os,sys
import subprocess
import multiprocessing as mp
import time 
from time import sleep 
import argparse

threads=8
outpath='output'
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='the path to reads folder')
parser.add_argument('-o', help='an output folder (dfault output)')
parser.add_argument('-t', help='threads (default=8)')
args = parser.parse_args()

argv=sys.argv
if '-t' in argv:
    threads=int(argv[argv.index('-t')+1])
if '-i' in argv:
    inpath=os.path.abspath(argv[argv.index('-i')+1])
if '-o' in argv:
    outpath=argv[argv.index('-o')+1]

outpath=os.path.abspath(outpath)

if not os.path.exists(outpath):
    os.mkdir(outpath)


def run(qfile,name,outpath):
    comm='medaka_consensus -i {0} -d /opt/nanoMLST2/SA_PCR-fullength.fa -o {2}/{1} -t {3}'.format(qfile,name,outpath,threads)
    print (comm)
    subprocess.getoutput(comm)

def main():
    po=mp.Pool(threads)
    for i in sorted(myfiles):
        qfile=os.path.join(inpath,i)
        name=i.split('.')[0]
        if os.path.exists(os.path.join(outpath,name)+'/consensus.fasta'):
            continue
        po.apply_async(run,[qfile,name,outpath])
    po.close()
    po.join()

os.chdir(inpath)
myfiles=[x for x in os.listdir() if 'fastq.gz' in x]
N=len(myfiles)
print (N)
if __name__=='__main__':
    po=mp.Pool(threads)
    for i in sorted(myfiles):
        qfile=os.path.join(inpath,i)
        name=i.split('.')[0]
        if os.path.exists(os.path.join(outpath,name)+'/consensus.fasta'):
            continue
        po.apply_async(run,[qfile,name,outpath])
    po.close()
    po.join()

for i in range(0,5):
    if __name__=='__main__':
        main()
    comm='ls {0}/*/consensus.fasta | wc -l'.format(outpath)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    countN=int(stdout)
    print (countN)
    if countN==N:
        break

os.chdir(outpath)
for i in sorted(myfiles):
    qfile=os.path.join(inpath,i)
    name=i.split('.')[0]
    comm='/opt/nanoMLST2/SA_MLSTtyping.py {1}/{0}/consensus.fasta'.format(name,outpath)
    print (comm)
    stdout=subprocess.getoutput(comm)
    print (stdout)
    with open (os.path.join(outpath,'log.txt') ,'a') as log:
        log.write(name+'\n'+stdout+'\n')
    with open (os.path.join(outpath,'SA_MLST_types.txt'), 'a') as types:
        lines=stdout.splitlines()
        types.write(name+'\t'+lines[-1]+'\n')

