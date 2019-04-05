# Data Acquisition

This folder contains code for downloading VCF files from the publicly available S3 Bucket to an Amazon EC2 instance. Each VCF file is parsed and the data is saved in sparse `scipy` COO matrices. To run the code, enter
```
./save_mats
```
from terminal in `<PROJECT_ROOT>/src/data_acq/`. It takes several hours and roughly 8 GB to download, parse, and save the entire dataset as sparse matrices.
