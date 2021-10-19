#!/usr/bin/env python3
import sys,os,subprocess
import argparse

threads=8
outpath='output'
parser = argparse.ArgumentParser()
parser.add_argument('-o', help='an output folder (dfault output)')
args = parser.parse_args()

argv=sys.argv
if '-o' in argv:
    outpath=argv[argv.index('-o')+1]

outpath=os.path.abspath(outpath)

if not os.path.exists(outpath):
    os.mkdir(outpath)
os.chdir(outpath)

if not os.path.exists('Staphylococcus_aureus'):
    os.mkdir('Staphylococcus_aureus')
os.chdir('Staphylococcus_aureus')

genes=['arcC','aroE','glpF','gmk','pta','tpi','yqiL']

comm='wget https://rest.pubmlst.org/db/pubmlst_saureus_seqdef/schemes/1/profiles_csv -O profile.txt'
print (comm)
subprocess.getoutput(comm)

for i in genes:
    comm='wget https://rest.pubmlst.org/db/pubmlst_saureus_seqdef/loci/{0}/alleles_fasta -O {0}.tfa'.format(i)
    print (comm)
    subprocess.getoutput(comm)

