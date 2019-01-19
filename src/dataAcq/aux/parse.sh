#!/usr/bin/env bash

VCFile="/home/ubuntu/data/variantCalls/chrom$@.vcf.gz"
parseFile="/home/ubuntu/src/dataAcq/bin/parse"
tsvFile="/home/ubuntu/data/processedVC/chrom$@.tsv"

zcat "$VCFile" | cut -f "10-" | "$parseFile" > "$tsvFile"
