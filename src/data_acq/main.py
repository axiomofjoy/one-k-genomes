"""
This script downloads VCF files for each chromosome from the pubicly
available S3 Bucket, parses each VCF file, and enters and saves the data
into a NumPy sparse matrix. It requires the PATH to
:code:`<PROJECT_ROOT>/` as a command-line argument. 
"""


import sys
import subprocess
import download_genomes as dg


def main():
    assert len(sys.argv) == 2, "Command-line argument is required."
    PATH = sys.argv[1]
    chroms = list(map(str, range(1,23))) + ['x', 'y']
    for chrom in chroms[:1]:
        # Display current chromosome.
        print("Chromosome: {:s}".format(chrom))

        # Get file names.
        if chrom == 'x':
            remote_file = ("s3://1000genomes/release/20130502/ALL.chrX."
                          "phase3_shapeit2_mvncall_integrated_v1b."
                          "20130502.genotypes.vcf.gz")
        elif chrom == 'y':
            remote_file = ("s3://1000genomes/release/20130502/ALL.chrY."
                          "phase3_integrated_v1b.20130502.genotypes.vcf."
                          "gz")
        else:   # The chromosome is a number.
            remote_file = ("s3://1000genomes/release/20130502/ALL.chr{:s}"
                          ".phase3_shapeit2_mvncall_integrated_v5a."
                          "20130502.genotypes.vcf.gz".format(chrom))

        local_file = "{:s}data/variant_calls/chrom{:s}.vcf.gz".format(
            PATH,
            chrom,
        )

        # Download sparse matrices.
        try:
            dg.get_sparse_mat(remote_file, local_file, chrom, PATH)
            
        except Exception as exc:
            print(str(exc))


if __name__ == "__main__":
    main()
