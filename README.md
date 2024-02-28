# Somatic_Cell_QC_Pipeline
Using methylation signatures, these pipelines identify somatic cell contamination in semen samples. Compatible with Illumina EPIC or 450K methylation data. 

#Set Up
1. Download your desired contamination detection model.
  **Somatic Cell QC Pipeline**: An simple algorithm that uses hypermethylation at 64 (Illumina EPIC Data) or 38 (Illumina 450K) genomic regions to detect somatic contamination.
**  Somatic Cell ML Pipeline**: A logistic regression model that uses hypermethylation at 250 regions to detect somatic contamination.

2. Set your input and output directories in _QC_bash_script.sh_
     # Path to base directory where you want your QC files to be generated. Don't forget to add a "/" at the end as we want the files to be created inside this directory.
  base_dir="/path/"
  
  # Path to beta values for your samples (Make sure it is a .csv file CG's are in the rows and sample names are in the columns)
  betas="/path2/"
  
  # Path to the dmrs folder you downloaded from the github. (This file can be downloaded from this github link: ) Don't forget to add a "/" at the end
  dmrs_path="/path3/"
  
  # Path to QC_python_script.py script
  python_script_path="/path4/"
