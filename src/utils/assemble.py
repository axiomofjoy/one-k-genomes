import numpy as np
import sys
import os
import re

def main():
	# Get path to project directory.
	assert(len(sys.argv) == 2), "Command line argument required."
	path = sys.argv[1]

	# Retrieve sorted data files.
	fullPath = path + "data/pdist/individualMats/"
	files = os.listdir(fullPath)
	isNumbered = lambda x: re.match("^pdist[0-9]+", x)
	numberFiles = list(filter(isNumbered, files))
	letterFiles = list(filter(lambda x: not isNumbered(x), files))

	# Add all matrices together.
	dim = 2504
	shape = (dim, dim)
	cumMat = np.zeros(shape)
	for count, file in enumerate(numberFiles):
		print(count + 1, ": ", file)
		mat = np.load(fullPath + file)
		cumMat += mat
	np.save(path + "data/pdist/summedMats/pdistNum.npy", cumMat)
	for count2, file in enumerate(letterFiles):
		print(count + count2 + 2, ": ", file)
		mat = np.load(fullPath + file)
		cumMat += mat
	np.save(path + "data/pdist/summedMats/pdistAll.npy", cumMat)


if __name__ == "__main__":
	main()
