### Paths to necessary files for Somatic Cell QC Pipeline

### Please replace the paths that were included for examples. Then input the paths to these directories as located on your machine. Make sure you are adding the paths inside the " " marks.

# Path to base directory where you want your QC files to be generated. Don't forget to add a "/" at the end as we want the files to be created inside this directory.
base_dir="/Users/carternorton/Desktop/temp/"

# Path to beta values for your samples (Make sure it is a .csv file CG's are in the rows and sample names are in the columns)
betas="/Users/carternorton/repo/Research/SomaticLike/SomaticCont/Contamination_Array_V2/Contamination_Array_beta_values.csv"

# Path to the dmrs folder you downloaded from the github. Don't forget to add a "/" at the end
dmrs_path="/Users/carternorton/Desktop/Somatic_Cell_ML_Pipeline/DMR_Files/"

# Path to QC_python_script.py script 
python_script_path="/Users/carternorton/Desktop/Somatic_Cell_ML_Pipeline/QC_python_script.py"

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

