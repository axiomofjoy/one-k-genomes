#!/usr/bin/env bash

path="/home/ubuntu/onekgenomes/"
vcfFile="data/variantCalls/chrom1.vcf.gz"
parseFile="src/dataAcq/parseDev/checkData"

zcat ${path}${vcfFile} | ${path}${parseFile}
