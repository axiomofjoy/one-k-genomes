import scipy.sparse as sparse
from functools import reduce
import sys
import os
import re

# Resize two matrices and add them together (implicitly converts to csr format).
def resizeAdd(A, B):
	shape = max(A.shape, B.shape)
	A.resize(shape)
	B.resize(shape)
	return A + B

# Resize two matrices and concatenate horizontally.
def resizeCat(A, B):
	numRows = max(A.shape[0], B.shape[0])
	A.resize((numRows, A.shape[1]))
	B.resize((numRows, B.shape[1]))
	return sparse.hstack([A, B])

# Given a list of chromosomes, forms the data matrix.
def formData(chroms, path):
	chromMats = list()
	for chrom in chroms:
		pattern = "^chrom" + chrom + "[-][0-9]+[.]npz"
		fullPath = path + "data/sparseMats/"
		files = list(filter(lambda x: re.match(pattern, x), os.listdir(fullPath)))
		mats = [sparse.load_npz(file) for file in files]
		chromMats.append(reduce(resizeAdd, mats))
	return reduce(resizeHStack, chromMats)

def main():
	assert(len(sys.argv) == 2), "One command line argument required"
	path = sys.argv[1]
	chroms = list(range(1,23)) + ["Y"]	#FIXME
	data = formData(chroms, path)


if __name__ == "__main__":
	main()
