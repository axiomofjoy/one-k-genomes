from functools import reduce
import scipy.sparse as sparse
import importData
import os
import re


def matNum(fileName):
	s = re.search("[-]([0-9]+)[.]npz$", fileName)
	if s is None:
		raise ValueError("Unexpected file format")
	return int(s.group(1))


@profile
def main():
	path = "/home/ubuntu/onekgenomes/"
	chrom = "1"
	pattern = "^chrom" + chrom + "[-][0-9]+[.]npz"
	fullPath = path + "data/sparseMats/"
	files = list(filter(lambda x: re.match(pattern, x), os.listdir(fullPath)))
	files.sort(key=matNum)
	files = [fullPath + file for file in files]
	"""#chromMat = reduce(importData.resizeAdd, mats)
	chromMat = sparse.csr_matrix((list(), (list(), list())), shape=(1, 1))
	for file in files:
	mat = sparse.load_npz(file)
	chromMat = importData.resizeAdd(chromMat, mat)
	print(chromMat.shape)

	"""

	mats = [sparse.load_npz(file) for file in files]
	A = reduce(importData.resizeAdd, mats)
	del mats
	print(A.count_nonzero() / (A.shape[0] * A.shape[1]))

if __name__ == "__main__":
	main()
