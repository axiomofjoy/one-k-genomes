"""
This script computes pairwise squared Euclidean distances matrices
(equivalently, pairwise Manhattan distance matrices) for the entire
dataset after pairwise distance matrices have been computed for each
sparse matrix.
"""


import sys
import os
import re
import numpy as np


def is_numbered(file_name):
    """
    This function checks whether the file name for a pairwise distance matrix
    corresponds to a numbered chromosome (1-23).

    The function takes as input a pairwise distance matrix file name satisfying
    the regular expression "^pdist.+". You acn
    :param:
    """

    return re.match("^pdist[0-9]+", file_name)


def main():
	# Get path to project directory.
	assert(len(sys.argv) == 2), "Command line argument required."
	PATH = sys.argv[1]

	# Retrieve sorted data files.
	FULL_PATH = PATH + "data/pdist/individual_mats/"
	files = os.listdir(FULL_PATH)
    	number_files = list(filter(is_numbered, files))
	letter_files = list(filter(lambda x: not is_numbered(x), files))

	# Add all matrices together.
	dim = 2504
	shape = (dim, dim)
	cum_mat = np.zeros(shape)
	for count, f in enumerate(number_files):
		print(count + 1, ": ", f)
		mat = np.load(FULL_PATH + f)
		cum_mat += mat
	np.save(path + "data/pdist/summed_mats/pdist_num.npy", cum_mat)
	for count_, f in enumerate(letter_files):
		print(count + count_ + 2, ": ", f)
		mat = np.load(FULL_PATH + f)
		cum_mat += mat
	np.save(path + "data/pdist/summed_mats/pdist_all.npy", cum_mat)


if __name__ == "__main__":
	main()
