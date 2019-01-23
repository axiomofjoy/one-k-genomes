#!/usr/bin/env bash

chrom=$1
path=$2
parser=$3
VCFile="${path}data/variantCalls/chrom${chrom}.vcf.gz"
parseFile="${path}src/dataAcq/bin/${parser}"
sparseMatFile="${path}src/dataAcq/aux/toSparseMat.py"

zcat $VCFile | $parseFile | python3 $sparseMatFile $chrom $path
