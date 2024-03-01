# Somatic_Cell_ML_Pipeline
Using region methylation signatures as features, this pipeline uses a logistic regression model to predict somatic cell contamination in sperm methylation data. 

## Required Environment Packages (Python):
pandas
numpy 
argparse
os 
sklearn

## FAQ
1. How does my input data need to be formatted?
Sample data should be a csv of normalized methylation beta values, with CpG's as the first column (index) and samples as the first row (header)
2. What methylation arrays does this tool support?
This tool is compatible with Infinium 450K and EPIC methylation array data
3. What does is the correlation between 'prediction' and 'predicted probability of contamination'?
Our model was designed with a threshold of 99.999% for non-contamination, meaning, it will generate a probability for a given sample not being contaminated, and if that probability is higher than 99.999%, then it will classify a sample as non-contaminated. 



