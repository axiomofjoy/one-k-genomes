import scipy.sparse as sparse
import sys


def saveSparseMat(rows, cols, matFile):
	data = [True] * len(rows)
	varMat = sparse.coo_matrix((data, (rows, cols)), dtype=bool)
	sparse.save_npz(matFile, varMat)

def main():
	assert (len(sys.argv) == 3), "Two command line arguments required."
	_, chrom, path = sys.argv
	rows, cols = list(), list()
	maxSize = 100000000
	matNum = 1
	for count, line in enumerate(sys.stdin):
		col, row = map(int, line.strip().split())
		rows.append(row)
		cols.append(col)
		if count % maxSize == maxSize - 1:
			matFile = path + "data/sparseMats/chrom" + chrom + "-" + str(matNum) + ".npz"
			saveSparseMat(rows, cols, matFile)
			rows, cols = list(), list()
			matNum = matNum + 1
	if rows:
		matFile = path + "data/sparseMats/chrom" + chrom + "-" + str(matNum) + ".npz"
		saveSparseMat(rows, cols, matFile)


if __name__ == '__main__':
	main()
