import subprocess
import sys

def main():
	path = sys.argv[1]
	chroms = list(map(str, range(1,23))) + ["X", "Y"]
	for chrom in chroms:
		print("Chromosome: " + chrom)
		try:
			# Download VCF file.
			if chrom == "X":
				remoteVCF = "s3://1000genomes/release/20130502/ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.vcf.gz"
			elif chrom == "Y":
				remoteVCF = "s3://1000genomes/release/20130502/ALL.chrY.phase3_integrated_v1b.20130502.genotypes.vcf.gz"
			else:
				remoteVCF = "s3://1000genomes/release/20130502/ALL.chr" + chrom + \
					".phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
			localName = "chrom" + chrom
			localVCF = path + "data/variantCalls/" + localName + ".vcf.gz"
			subprocess.run(["s3cmd", "get", remoteVCF, localVCF])

			# Parse VCF file and save data in sparse matrices.
			pipeFile = path + "src/dataAcq/aux/pipe.sh"
			parser = "parseY" if chrom == "Y" else "parse"
			subprocess.run([pipeFile, chrom, path, parser])

			# Remove VCF file.
			subprocess.run(["rm", localVCF])

		except Exception as exc:
			# Print exceptions to stdout. Check nohup.out if running main with nohup.
			print(str(exc))

if __name__ == '__main__':
	main()
