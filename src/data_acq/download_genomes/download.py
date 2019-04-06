"""
This script downloads VCF files for each chromosome from the pubicly
available S3 Bucket, parses each VCF file, and enters and saves the data
into a NumPy sparse matrix. It requires the path to
:code:`<PROJECT_ROOT>/` as a command-line argument. 
"""


__all__ = ["get_sparse_mat"]


import subprocess


def get_sparse_mat(remote_file, local_file, chrom, path):
    """
    This script downloads a VCF file from the 1000 Genomes S3 Bucket,
    calls "pipe.sh" to parse the file and save the data in :code:`scipy`
    sparse COO matrices, and then deletes the downloaded VCF file. The
    AWS CLI should be successfully installed before running this script.

    :param remote_file str: Name of VCF file in S3 Bucket.
    :param str local_file: Full-path file name specifying where the
        downloaded VCF file will be temporarily saved.
    :param str chrom: Chromosome number or letter.
    :param str path: Path to :code:`<PROJECT_ROOT>`.
    :return: Nothing
    :rtype: :code:`None`

    """

    # Download VCF file.
    subprocess.run(["s3cmd", "get", remote_file, local_file])

    # Parse VCF file and save data in sparse matrices.
    pipe_file = "{:s}/src/data_acq/download_genomes/pipe.sh".format(path)
    parser = "parse_y" if chrom == 'y' else "parse"
    subprocess.run([pipe_file, chrom, path, parser])

    # Remove VCF file.
    subprocess.run(["rm", local_file])
