import re
import sys
import scipy.sparse as sparse
import numpy as np
from matFiles import fileNames
from sklearn.metrics.pairwise import manhattan_distances, euclidean_distances
from random import randint


def test(X, pdistMat, i, j):
	entry = np.abs(X[i,:] - X[j,:]).sum()
	return entry == pdistMat[i,j]


def main():
	# Get path to project directory.
	assert(len(sys.argv) == 2), "Command line argument required."
	path = sys.argv[1]

	# Retrieve sorted data files.
	fullPath = path + "data/sparseMats/"
	files = fileNames(fullPath)

	# Parameters.
	numRows = 2504	# Number of samples in data set

	# Iterate through matrices and calculate partial pairwise distance matrices.
	for count, file in enumerate(files):
		# Display progress.
		print(str(count + 1) + "/" + str(len(files)), file)

		# Load data and ensure it has proper number of rows.
		X = sparse.load_npz(fullPath + file).tocsr()
		X.resize((numRows, X.shape[1]))

		# Compute pairwise distances and save to file.
		pdistMat = euclidean_distances(X, squared=True)
		m = re.match("^chrom([0-9]+|X|Y)[-]([0-9]+)[.]npz$", file)
		pdistFile = path + "data/pdist/individualMats/" + "pdist" + m.group(1) + "-" + m.group(2) + ".npy"
		np.save(pdistFile, pdistMat)

		for t in range(5):
			i, j = randint(0, numRows - 1), randint(0, numRows - 1)
			test(X, pdistMat, i, j)
			testResult = test(X, pdistMat, i, j)
			print("Test Entry Success: ", i, j, testResult)

if __name__ == "__main__":
	main()





