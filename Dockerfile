FROM nvidia/cuda:11.1-devel-ubuntu20.04 
ENV http_proxy=http://proxy.nhri.org.tw:3128 
ENV https_proxy=http://proxy.nhri.org.tw:3128 
ENV TZ=Asia/Taipei 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone 
RUN apt-get update && apt-get install -y \ 
    python3 python\ 
    python3-pip \ 
    python3-setuptools \ 
    python3-dev \ 
    libbz2-dev \ 
    liblzma-dev \ 
    libncurses5-dev \ 
    libncursesw5-dev \ 
    zlib1g-dev \ 
    libcurl4-gnutls-dev libssl-dev \ 
    cmake unzip git wget libz-dev vim autoconf curl 
RUN pip3 install biopython pandas lxml six ete3 medaka==1.4.3 numpy==1.18.5
#Download nanoMLST2 
WORKDIR /opt 
RUN git clone https://github.com/jade-nhri/nanoMLST2.git 
WORKDIR /opt/nanoMLST2/ 
RUN chmod +x *.py 
#samtools 1.13 
ADD https://github.com/samtools/samtools/releases/download/1.13/samtools-1.13.tar.bz2 /opt 
RUN apt-get update && apt-get install -y \ 
    libncurses-dev \ 
    apt-file \ 
    liblzma-dev \ 
    libz-dev \ 
    libbz2-dev \ 
    vim parallel 
WORKDIR /opt 
RUN tar -xjf /opt/samtools-1.13.tar.bz2 
WORKDIR /opt/samtools-1.13 
RUN make && make install 
WORKDIR / 
#Install htslib 
WORKDIR /opt 
RUN git clone https://github.com/samtools/htslib.git 
WORKDIR /opt/htslib 
RUN git submodule update --init --recursive 
RUN autoreconf -i 
RUN ./configure 
RUN make 
RUN make install 
#Install bcftools 
WORKDIR /opt 
RUN git clone https://github.com/samtools/bcftools.git 
WORKDIR /opt/bcftools 
RUN make 
RUN make install 
#Minimap2, miniasm 
#2.20-r1061 
 WORKDIR /opt 
RUN curl -L https://github.com/lh3/minimap2/releases/download/v2.20/minimap2-2.20_x64-linux.tar.bz2 | tar -jxvf - 
RUN mv minimap2-2.*/ minimap2 
#Install seqkit 0.15 
WORKDIR /opt 
RUN wget https://github.com/shenwei356/seqkit/releases/download/v0.15.0/seqkit_linux_amd64.tar.gz 
RUN tar -zxvf seqkit_linux_amd64.tar.gz 
RUN cp seqkit /usr/local/bin 
WORKDIR / 
#set path 
ENV PATH $PATH:/opt:/opt/nanoMLST2/:/opt/minimap2/:/opt/samtools-1.13:/opt/hstlib:/opt/bcftools
