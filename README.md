# Somatic_Cell_QC_Pipeline
Using methylation signatures, these pipelines identify somatic cell contamination in semen samples. Compatible with Illumina EPIC or 450K methylation data. 

# Set Up
## 1. Download your desired contamination detection model. <br>
   
  **Somatic Cell QC Pipeline**: An simple algorithm that uses hypermethylation at 64 (Illumina EPIC Data) or 38 (Illumina 450K) genomic regions to detect somatic contamination. <br>
  **Somatic Cell ML Pipeline**: A logistic regression model that uses hypermethylation at 250 regions to detect somatic contamination.

## 2. Set your input and output directories in _QC_bash_script.sh_ 

<img width="1258" alt="Screen Shot 2024-02-27 at 8 10 07 PM" src="https://github.com/jenkins-lab-byu/Somatic_Cell_QC_Pipeline/assets/99043737/012d2502-ae71-4c54-8068-f45697cca48c">

## 3. Run your bash script in terminal <br>
   bash /path/QC_bash_script.sh

## 4. Check results

| Sample_ID | Data_Type | Total_DMRS_Analyzed | Contamination_Score | Mean_DLK1 | Contamination_Call                              |
|-----------|-----------|----------------------|----------------------|-----------|--------------------------------------------------|
| X10001    | EPIC      | 64                   | 5                    | 0.1068    | Likely NOT Contaminated with Somatic Cells       |
| X10002    | EPIC      | 64                   | 6                    | 0.1201    | Likely NOT Contaminated with Somatic Cells       |
| X10003    | EPIC      | 64                   | 7                    | 0.1257    | Likely NOT Contaminated with Somatic Cells       |

