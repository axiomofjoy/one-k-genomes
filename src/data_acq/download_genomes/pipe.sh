#!/usr/bin/env bash

chrom=$1
path=$2
parser=$3
vcf_file="${path}data/variant_calls/chrom${chrom}.vcf.gz"
parse_file="${path}src/data_acq/download_genomes/bin/${parser}"
sparse_mat_file="${path}src/data_acq/download_genomes/to_sparse_mat.py"

zcat $vcf_file | $parse_file | python3 $sparse_mat_file $chrom $path
