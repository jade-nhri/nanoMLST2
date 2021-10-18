#!/usr/bin/env python3
import os,sys
import subprocess

outdir=sys.argv[1]
outdir=os.path.abspath(outdir)


if not os.path.exists(outdir):
    os.mkdir(outdir)


os.chdir(outdir)
comm='wget https://pubmlst.org/static/data/dbases.xml'
print (comm)
subprocess.getoutput(comm)


print (os.getcwd())
if os.path.exists('dbases.xml'):
    d=dict()
    f=open('dbases.xml')
    while True:
        l=f.readline()
        if not l: break
        if l.startswith('<species>') and '/' not in l:
            spe=l.replace('<species>','').replace('\n','').replace(' spp.','').replace(' ','_')
            #print (spe)
            os.mkdir(spe)
            os.chdir(spe)
            continue
        if l.startswith('<species>') and '/' in l:
            spe=l.replace('<species>','').replace('\n','').replace(' ','_')
            spe=spe.split('/')[0]
            print (spe)
            os.mkdir(spe)
            os.chdir(spe)
            continue
        if l.startswith('<url>'):
            url=l.replace('<url>','').replace('</url>','').replace('\n','')
            #print (url)
            if 'profiles' in url:
                comm='wget {0} -O profile.txt'.format(url,spe)
                #print (comm)
                subprocess.getoutput(comm)
            if 'alleles' in url:
                gene=url.split('/')[-2]
                comm='wget {0} -O {1}.tfa'.format(url,gene)
                #print (comm)
                subprocess.getoutput(comm)
            continue
        if l.startswith('</species'):
            #print (os.getcwd())
            os.chdir('..')
            continue
