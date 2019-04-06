"""
This script reads in pairs of :code:`int`s from :code:`stdin` indicating
non-zero entries in the data matrix. For each pair, it adds a non-zero
entry to a :code:`scipy` sparse COO matrix. These matrices are
periodically saved to disk. It requires two command-line arguments
specifying the chromosome and the full path to :code:`<PROJECT_ROOT>`.
"""
 

import sys
import scipy.sparse as sparse


# Define constant.
MAX_SIZE = 1e8


def save_sparse_mat(rows, cols, mat_file):
    """
    This function creates and saves :code:`scipy` sparse matrices.

    Given lists of row and column indices, this function adds non-zero
    entries in a :code:`scipy` sparse COO matrix and save the matrix to
    disk as a :code:`.npy` file.

    :param list rows: Row indices for non-zero entries.
    :param list cols: Column indices for non-zero entries.
    :returns: Nothing.
    :rtype: :code:`None`.

    """

    data = [True] * len(rows)
    var_mat = sparse.coo_matrix((data, (rows, cols)), dtype=bool)
    sparse.save_npz(mat_file, var_mat)


def main():
    # Get chromosome and path from command line.
    assert (len(sys.argv) == 3), ("This script requires two command-line"
                                  "arguments.")
    _, chrom, path = sys.argv

    # Initialize variables.
    rows, cols = list(), list()
    mat_num = 1

    # Read from stdin.
    for count, line in enumerate(sys.stdin):
        col, row = map(int, line.strip().split())
        rows.append(row)
        cols.append(col)

        # Write to file when matrix has MAX_SIZE entries.
        if count % MAX_SIZE == MAX_SIZE - 1:
            mat_file = "{:s}data/sparse_mats/chrom{:s}-{:s}.npz".format(
                path,
                chrom,
                str(mat_num),
            )
            save_sparse_mat(rows, cols, mat_file)
            rows, cols = list(), list()
            mat_num = mat_num + 1
    

    if rows:
        mat_file = "{:s}data/sparse_mats/chrom{:s}-{:s}.npz".format(
            path,
            chrom,
            str(mat_num),
        )
        save_sparse_mat(rows, cols, mat_file)


if __name__ == "__main__":
    main()
