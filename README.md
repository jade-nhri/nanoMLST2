# nanoMLST2
Accurate multilocus sequence typing using Oxford Nanopore MinION for multiplex polymerase chain reaction

**To run with Docker**

git clone https://github.com/jade-nhri/nanoMLST2.git

cd nanoMLST2

docker build -t "nanomlst2:v1" ./

docker run -h nanomlst2 --name nanomlst2 -t -i -v /:/MyData nanomlst2:v1 /bin/bash

**Installation**

Installation from source

cd /opt

git clone https://github.com/jade-nhri/nanoMLST2.git

cd nanoMLST2

chmod +x *.py

export PATH="$PATH:/opt/nanoMLST2"
