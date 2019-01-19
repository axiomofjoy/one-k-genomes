import re
import csv
import scipy.sparse as sparse
import sys
import pandas as pd
import numpy as np

def tsvToSparseMat(tsvFile, matFile):
	if not re.match(r".*\.npz$", matFile):
		raise ValueError("matFile must end in '.npz'")

	df = pd.read_csv(tsvFile, sep="\t", names=["Site", "Person"],
		 dtype={"Site": int, "Person": int})
	rows, cols = df["Person"].values, df["Site"].values
	data = np.ones(rows.shape, dtype=bool)
	varMat = sparse.coo_matrix((data, (rows, cols)), dtype=bool)
	sparse.save_npz(matFile, varMat)

	return


if __name__ == '__main__':
	assert (len(sys.argv) == 3), "Two command line arguments required."
	args = sys.argv[1:]
	tsvToSparseMat(*args)
