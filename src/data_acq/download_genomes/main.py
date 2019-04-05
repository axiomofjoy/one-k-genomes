"""
This script downloads VCF files for each chromosome from the pubicly
available S3 Bucket, parses each VCF file, and enters and saves the data
into a NumPy sparse matrix. It requires the path to
:code:`<PROJECT_ROOT>/` as a command-line argument. 
"""


import sys
import subprocess


def main():
    assert len(sys.argv) == 2, "Command-line argument is required."
    path = sys.argv[1]
    chroms = list(map(str, range(1,23))) + ['x', 'y']
    for chrom in chroms[:1]:
        print("Chromosome: " + chrom)
        try:
            # Download VCF file.
            if chrom == 'x':
                remote_vcf = ("s3://1000genomes/release/20130502/ALL.chrX."
                              "phase3_shapeit2_mvncall_integrated_v1b."
                              "20130502.genotypes.vcf.gz")
            elif chrom == 'y':
                remote_vcf = ("s3://1000genomes/release/20130502/ALL.chrY."
                              "phase3_integrated_v1b.20130502.genotypes.vcf."
                              "gz")
            else:
                remote_vcf = ("s3://1000genomes/release/20130502/ALL.chr{:s}"
                              ".phase3_shapeit2_mvncall_integrated_v5a."
                              "20130502.genotypes.vcf.gz".format(chrom))
            local_name = "chrom{:s}".format(chrom)
            local_vcf = "{:s}data/variant_calls/{:s}.vcf.gz".format(
                path,
                local_name,
            )
            subprocess.run(["s3cmd", "get", remote_vcf, local_vcf])

            # Parse VCF file and save data in sparse matrices.
            pipe_file = "{:s}src/data_acq/download_genomes/pipe.sh".format(path)
            parser = "parse_y" if chrom == 'y' else "parse"
            subprocess.run([pipe_file, chrom, path, parser])

            # Remove VCF file.
            subprocess.run(["rm", local_vcf])

        except Exception as exc:
            # Check nohup.out for exceptions.
            print(str(exc))

if __name__ == "__main__":
    main()
