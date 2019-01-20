import scipy.sparse as sparse
import subprocess
import sys
import vcf
import time

path = sys.argv[1]

def main():
	chroms = list(map(str, range(1,23)))
	for chrom in chroms:
		print("Chromosome: " + chrom)
		try:
			# Download VCF file.
			fileName = "s3://1000genomes/release/20130502/ALL.chr" + chrom + \
				".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
			localName = "chrom" + chrom
			vCDir = path + "data/variantCalls/"
			procDir = path + "data/processedVC/"
			matDir = path + "data/sparseMats/"
			subprocess.run(["s3cmd", "get", fileName, vCDir + localName + ".vcf.gz"])

			# Parse VCF file, enter variants into sparse coo matrix, and write to file.
			vcfReader = vcf.Reader(filename=(vCDir + localName + ".vcf.gz"))
			rows, cols = list(), list()
			t = time.time()
			for colCount, record in enumerate(vcfReader):
				if colCount % 1000 == 0:
					print(t - time.time())
				for rowCount, sample in enumerate(record.samples):
					if sample["GT"] != "0|0":
						rows.append(rowCount)
						cols.append(colCount)
			data = [True] * len(rows)
			varMat = sparse.coo_matrix((data, (rows, cols)), shape=(rowCount + 1, colCount + 1), dtype=bool)
			sparse.save_npz(matDir + localName, varMat)

			# Delete VCF file.
			subprocess.run(["rm", vCDir + localName + ".vcf.gz"])

		except Exception as exc:
			errFile = path + "err/dataAcqErrors.txt"
			fileID = open(errFile, 'a')
			fileID.write("Chromosome: " + chrom + "\n")
			fileID.write(str(exc) + "\n")
			fileID.close()

if __name__ == '__main__':
	main()
