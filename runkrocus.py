#!/usr/bin/env python3
import os,sys
import subprocess
import multiprocessing as mp
import argparse

threads=8
outpath='output'
parser = argparse.ArgumentParser()
parser.add_argument('-i', help='the path to raw_reads folder')
parser.add_argument('-t', help='threads (default=8)')
args = parser.parse_args()

argv=sys.argv
if '-t' in argv:
    threads=int(argv[argv.index('-t')+1])
if '-i' in argv:
    inpath=os.path.abspath(argv[argv.index('-i')+1])

cwd=os.getcwd()

def run(bc):
    comm='krocus -p 4000 {2}/Staphylococcus_aureus {0}/{1}/*_0.fastq*'.format(inpath,bc,cwd)
    #print (comm)
    stdout=subprocess.getoutput(comm)
    stdoutline=stdout.split('\n')
    #print (len(stdoutline))
    #print (stdout)
    for line in stdoutline:
        #fw=open(outfile,'a')
        #fw.write('{0}\t{1}\n'.format(bc,line))
        lastline=line
    #fw.close()
    print ('{0}\t{1}\n'.format(bc,lastline))
    


os.chdir(inpath)
myfiles=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
print (myfiles)

def main():
    po=mp.Pool(threads)
    for i in myfiles:
        po.apply_async(run,[i])
    po.close()
    po.join()
if __name__=='__main__':
    main()

