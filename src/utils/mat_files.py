import scipy.sparse as sparse
import sys
import os
import re


def matTuple(fileName):
	m = re.match("^chrom([0-9]+|X|Y)[-]([0-9]+)[.]npz$", fileName)
	if m is None:
		raise ValueError("Unexpected file format")
	firstElem = m.group(1)
	if firstElem.isdigit():
		firstElem = int(firstElem)
	return (firstElem, int(m.group(2)))

def fileNames(fullPath):
	files = os.listdir(fullPath)
	isNumbered = lambda x: re.match("^chrom[0-9]+.+", x)
	numberFiles = list(filter(isNumbered, files))
	letterFiles = list(filter(lambda x: not isNumbered(x), files))
	numberFiles.sort(key=matTuple)
	letterFiles.sort(key=matTuple)
	return numberFiles + letterFiles

def main():
	assert(len(sys.argv) == 2), "Requires command line argument"
	path = sys.argv[1]
	fullPath = path + "data/sparseMats/"
	files = fileNames(fullPath)
	for file in files:
		print(file)

if __name__ == "__main__":
	main()
