import numpy as np


def laplacianKernel(gamma, pdistFile):
	pdistMat = np.load(pdistFile)
	return np.exp(-gamma * pdistMat)
