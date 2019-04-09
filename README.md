# 1000 Genomes

This project applies supervised and unsupervised learning to human genomic data. In particular, it applies kernel PCA with linear and RBF kernels to visualize the data in two and three dimensions. It also uses SVMs and neural networks to classify each individual genome as belonging to one of 25 "populations" (roughly, ethnic groups). For an in-depth description of the application of kernel PCA and to view the dataset in lower dimensions, refer to the blog post [here](https://www.axiom-of-joy.com/2019/02/19/genome_part_i.html). A blog post describing the use of SVMs and neural networks to predict individual ethnic origin will be posted soon.


## Dataset

The dataset for this project is the 1000 Genomes Project, an international effort to catalogue human genetic variation commencing in 2008 and concluding in 2015. The dataset includes 2504 human genomes sequenced at roughly 81 million so-called "variant sites", i.e., loci on the genome that frequently vary between different individuals. Each individual sample belongs to one of 26 "populations" (roughly, ethnic groups) and one of five "super populations" (roughly, racial groups) from around the world.

The 1000 Genomes dataset is publicly available as an AWS S3 Bucket.


## Variant Call Format

The project The following excerpt illustrates the variant call format (for clarity, most columns have been omitted and the text has been formatted so that columns are properly aligned).

```
#CHROM  POS     REF     ALT     HG00096 HG00097 HG00099 HG00100 HG00101
1       10177   A       AC      1|0     0|1     0|1     1|0     0|0
```

The second row above corresponds to a variant site located in the first chromosome at position 10177. The reference genome has adenine at this site, while certain individuals have both adenine and cytosine. Identification codes uniquely identify each individual in the study (e.g., “HG00096”). Below these ID codes, the digits to the left and right of the pipe signify whether the reference or alternate sequence are present on the left and right alleles of the corresponding sample, with zero corresponding to the reference sequence and one corresponding to the alternate sequence. For example, sample HG00096 has the variant AC on the left allele and the reference sequence A on the right allele at position 10177 of the first chromosome. In certain cases (not shown above), multiple alternate sequences may be given, in which case positive digits indicate which variant is present. This format applies for chromosomes 1 through 21 and the X chromosome. Since human beings possess at most one allele for the Y chromosome, the VCF entries for this chromosome consist of single digits rather than digits separated by a pipe. In rare cases, a period indicates that data is missing for a particular sample and site.


## Requirements and Installation

This project was implemented in Python3 on an AWS t2.xlarge EC2 instance with Ubuntu 18.04 LTS and 16 GB of storage. Downloading the VCF files from the S3 Bucket requires the AWS CLI, which can be installed by entering

```
sudo apt-get update
```

and then

```
sudo apt-get install awscli
```

Then install the package management system `pip` with

```
sudo apt install python3-pip
```

and enter

```
pip3 install -r requirements.txt
```

to install the required Python modules. Depending on your setup, you might want to set up a virtual environment with `virtualenv` before this last step.
