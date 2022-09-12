### Paths to necessary files for Somatic Cell QC Pipeline

### Please replace the paths that were included for examples. Then input the paths to these directories as located on your machine. Make sure you are adding the paths inside the " " marks.

# Path to base directory where you want your QC files to be generated. Don't forget to add a "/" at the end as we want the files to be created inside this directory.
base_dir="/Volumes/Research_Data/Research_Datasets/Sperm/Blood_Sperm/Jenkins-BYU_MethylationEPIC_20201221_bad_samples_removed/Contamination_Analysis/"

# Path to beta values for your samples (Make sure it is a .csv file CG's are in the rows and sample names are in the columns)
betas="/Volumes/Research_Data/Research_Datasets/Sperm/Blood_Sperm/Jenkins-BYU_MethylationEPIC_20201221_bad_samples_removed/Jenkins-BYU_MethylationEPIC_20201221_bad_samples_removed_beta_values.csv"

# Path to the dmrs folder you downloaded from the github. (This file can be downloaded from this github link: ) Don't forget to add a "/" at the end
dmrs_path="/Volumes/Research_Data/Jenkins_Lab_Github/Somatic_Cell_QC_Pipeline/DMR_Files/"

# Path to QC_python_script.py script (This file can be downloaded from this github link: )
python_script_path="/Volumes/Research_Data/Jenkins_Lab_Github/Somatic_Cell_QC_Pipeline/QC_python_script.py"


######################################################
## DO NOT CHANGE ANY OF THE CODE BEYOND THIS POINT ###
######################################################

#################################
## Creating Output Directories ##
#################################
echo ""
echo "**** Creating Output Directories ****"

# Change to USEQ_prep directory
cd $base_dir
mkdir Figures
mkdir Reports


#########################
## Running QC Pipeline ##
#########################
echo ""
echo "**** Running QC_python_script.py ****"
echo ""


python $python_script_path --base_dir $base_dir --betas $betas --dmrs_path $dmrs_path

##########################
## Finished QC Pipeline ##
##########################
# echo ""
# echo "Finished! Your QC files and figures can be found in the directory: $base_dir"
# echo ""

