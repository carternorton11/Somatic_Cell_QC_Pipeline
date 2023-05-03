print("Loading Packages...")

print("importing pandas as pd")
import pandas as pd
print("importing numpy as np")
import numpy as np
print("importing argparse")
import argparse
print("importing os")
import os
print("importing sklearn")
import sklearn

## Define Functions
def get_region_means(regions, df):
  chrset = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chr10","chr11","chr12","chr13", "chr14", "chr15", "chr16", "chr17","chr18", "chr19", "chr20", "chr21", "chr22", "chrX", "chrY"]
  results_mean = pd.DataFrame()

  #Main Region Function
  first = True
  for chr in chrset:
    chr_regions = pd.DataFrame()
    df_regions = pd.DataFrame()
    chr_regions = regions[regions["CHR"] == chr]
    df_regions = df[df["CHR"] == chr]
    #print(df_regions)
    
    for index in chr_regions.index:
      #create temp array for holding start and stop values of a region
      ## Decide here if you want NEW (trimmed) or OLD regions
      Start = chr_regions.loc[index, "Start"]
      Stop = chr_regions.loc[index, "Stop"]
      #select for only CpG's within the given region
      r = df_regions[(df_regions["Location"] >= Start) & (df_regions["Location"] <= Stop)]
      r = r.drop(["CHR", "Location"], axis = 1)
      ### r = r.drop(["CHR", "Location", "CHR.1", "Location.1"], axis = 1)
      #track the number of CpG's in given region
      l = len((r.index))
      r = r.apply(np.nanmean) #remove na's ??
      #calculate the mean of the row, rewrite itself
      anno_series = pd.Series(dtype=object)
      anno_series["Name"] = f"{chr}:{int(Start)}-{int(Stop)}"
      anno_series["CHR"] = chr
      anno_series["Start"] = Start
      anno_series["Stop"] = Stop
      anno_series["CPG_Count"] = l
      r = pd.concat([anno_series,r])
      r = (r.to_frame()).T 
      if first == True:
        results_mean= r
        first = False
      else:
        results_mean = pd.concat([results_mean,r], axis=0)

  results_mean.index = results_mean["Name"]
  results_mean = results_mean.drop(["Name"],axis=1)
  results_mean = results_mean.rename_axis(None, axis=0) #remove index title

  #Let's remove all the extra info
  clean_results_mean = results_mean.iloc[:,4:]
  return clean_results_mean

def getBinary(df, summary):
    output = pd.DataFrame(index=df.index, columns=df.columns)

    #drop all summary columns that are not in df
    summary = summary[summary.index.isin(df.index)]

    for i, row in df.iterrows():
        for j, x in row.iteritems():
            if (x > summary.loc[i, "mean+2std"]) or (x < summary.loc[i, "mean-2std"]):
                output.loc[i, j] = 1
            else:
                output.loc[i, j] = 0
    return output

###############
## ARGUMENTS ##
###############
##  Add Arguments from command line
parser=argparse.ArgumentParser(description='Generating QC Files')
parser.add_argument('--base_dir', help='Path to base directory where you would like QC reports to be generated',type=str, required=True)
parser.add_argument('--betas', help='Path to beta values',type=str, required=True)
parser.add_argument('--dmrs_path', help='Path to DMR_Files folder',type=str, required=True)

## get arguments
args = parser.parse_args()
base_dir=args.base_dir
betas=args.betas
dmrs_path=args.dmrs_path

# Set directory to the base directory. This is where you want the QC files to be generated.
path_to_my_dir = base_dir
os.chdir(path_to_my_dir)
print("")
print("Home Directory Has Been Set to", path_to_my_dir)

# Read in Betas, Treatment Betas, and the desired annotation file (This one is EPIC)
print("")
print("Reading in DMR Files")
dmrs= pd.read_csv(dmrs_path + "DMRs.csv",header = 0)
cutoffs = pd.read_csv(dmrs_path + "cutoffs.csv",header = 0,index_col = 0)

print("Reading in Beta Values")
beta_values = pd.read_csv(betas,header = 0,index_col = 0)





# Identifies array type, and builds the appropriate dictionary using the dmr files that were read in the previous step
if len(beta_values) > 500000:
    print("")
    print("***** This looks like EPIC 850K Data ****")
    print("")
    data_type = "EPIC"
if len(beta_values) < 500000:
    print("")
    print("**** This looks like 450K Data ****")
    print("")
    data_type = "450K"
if len(beta_values) < 30000:
    print("")
    print("***** This looks like 27K data. REMINDER THIS PIPELINE WILL NOT WORK FOR ANY OTHER PLATFORM BUT 450K AND 850K METHYLATION ARRAY DATA")
    print("")

print("Number of CG's Identified:", len(beta_values))
print("")
print(beta_values)

#Let's load in the annotation files
print("Loading in Annotation Files")
if data_type == "EPIC":
    anno = pd.read_csv(dmrs_path + "Anno/epic_anno.csv",header = 0, index_col = 0)
if data_type == "450K":
    anno = pd.read_csv(dmrs_path + "Anno/450K_anno.csv", index_col = 0)

#Let's merge the betas and annotation files
anno_betas = pd.merge(anno, beta_values, left_index=True, right_index=True)
anno_betas

#Let's get the mean beta values for each region
mean_betas = get_region_means(dmrs, anno_betas)
mean_betas

#Let's get the binary values for each region
beta_binary = getBinary(mean_betas, cutoffs).T
beta_binary

import pickle

# Open the file containing the pickle object
with open(dmrs_path + 'LR_model.sav', 'rb') as file:
    # Load the object from the file
    LR_model = pickle.load(file)

# Use the loaded model to make predictions
threshold = .99999 #Model must be 99.999% sure that the sample is uncontaminated to classify as uncontaminated
proba = LR_model.predict_proba(beta_binary)
binary_pred = ["Uncontaminated" if x[1] > threshold else "Contaminated" for x in proba]

binary_pred = pd.DataFrame(binary_pred, index = beta_binary.index, columns = ["Prediction"])

#Add a probability column to the dataframe
binary_pred["Predicted_Probability_of_Contamination_%"] = [((1 - x[1]) * 100) for x in proba]
binary_pred.to_csv(base_dir + "Predictions.csv")












