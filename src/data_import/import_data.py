import scipy.sparse as sparse
from functools import reduce
import sys
import os
import re

# Resize two matrices and add them together (implicitly converts to csr format).
def resize_add(A, B):
	shape = max(A.shape, B.shape)
	A.resize(shape)
	B.resize(shape)
	return A + B

# Resize two matrices and concatenate horizontally.
def resize_cat(A, B):
	num_rows = max(A.shape[0], B.shape[0])
	A.resize((num_rows, A.shape[1]))
	B.resize((num_rows, B.shape[1]))
	return sparse.hstack([A, B])

# Given a list of chromosomes, forms the data matrix.
def form_data(chroms, path):
	chrom_mats = list()
	for chrom in chroms:
		pattern = "^chrom" + chrom + "[-][0-9]+[.]npz"
		full_path = path + "data/sparse_mats/"
		files = list(filter(lambda x: re.match(pattern, x), os.listdir(full_path)))
		mats = [sparse.load_npz(file) for file in files]
		chrom_mats.append(reduce(resize_add, mats))
	return reduce(resizeHStack, chrom_mats)

def main():
	assert(len(sys.argv) == 2), "One command line argument required"
	path = sys.argv[1]
	chroms = list(range(1,23)) + ["Y"]	#FIXME
	data = form_data(chroms, path)


if __name__ == "__main__":
	main()
