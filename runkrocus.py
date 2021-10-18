#!/usr/bin/env python3
import os,sys
import subprocess
import multiprocessing as mp

indir=os.path.abspath(sys.argv[1])
cwd=os.path.abspath(os.getcwd())


def run(bc):
    comm='krocus -p 4000 {2}/Staphylococcus_aureus {0}/{1}/*_0.fastq*'.format(indir,bc,cwd)
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
    


os.chdir(indir)
myfiles=[x for x in os.listdir() if os.path.isdir(x) and 'barcode' in x]
print (myfiles)

def main():
    po=mp.Pool(96)
    for i in myfiles:
        po.apply_async(run,[i])
    po.close()
    po.join()
if __name__=='__main__':
    main()

