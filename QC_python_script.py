print("Loading Packages...")

print("importing pandas as pd")
import pandas as pd
print("importing numpy as np")
import numpy as np
print("importing seaborn as sns")
import seaborn as sns
print("importing matplotlib.pyplot as plt")
import matplotlib.pyplot as plt
print("importing argparse")
import argparse
print("importing os")
import os

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
dmrs_EPIC = pd.read_csv(dmrs_path + "EPIC_dmrs_start_stop_positions.csv",header = 0)
dmrs_450K = pd.read_csv(dmrs_path + "450K_dmrs_start_stop_positions.csv",header = 0)
cutoffs_EPIC = pd.read_csv(dmrs_path + "EPIC_dmrs_cutoffs.csv",header = 0,index_col = 0)
cutoffs_450K = pd.read_csv(dmrs_path + "450K_dmrs_cutoffs.csv",header = 0,index_col = 0)
print("Reading in Beta Values")
beta_values = pd.read_csv(betas,header = 0,index_col = 0)
print("")
print("Number of CG's Identified:", len(beta_values))
print("")
print(beta_values)





# Identifies array type, and builds the appropriate dictionary using the dmr files that were read in the previous step
if len(beta_values) > 500000:
    print("")
    print("***** This looks like EPIC 850K Data ****")
    print("")
    dmrs = dmrs_EPIC
    data_type = "EPIC"
if len(beta_values) < 500000:
    print("")
    print("**** This looks like 450K Data ****")
    print("")
    dmrs = dmrs_450K
    data_type = "450K"
if len(beta_values) < 30000:
    print("")
    print("***** This looks like 27K data. REMINDER THIS PIPELINE WILL NOT WORK FOR ANY OTHER PLATFORM BUT 450K AND 850K METHYLATION ARRAY DATA")
    print("")

dmrs_dict = {}
count = 0
for index in dmrs.index:
    key = dmrs.loc[index,"REGION"]
    value = dmrs.loc[index,"CG"]

    if key not in dmrs_dict:
        dmrs_dict[key] = [value]
    else:    
        dmrs_dict[key].append(value)

print("Number of DMR'S Used for Contamination QC Analysis:", len(dmrs_dict))




# Builds dataframe that calculates the mean beta value across each dmr (and dlk1), for each sample. Then saves this dataframe as a .csv in the Reports folder.
print("")
print("Calculating Mean DMR Beta Values for Each Sample")
mean_dmr_df=pd.DataFrame()
count = 0
for key in dmrs_dict:
    count += 1
    beta_key = beta_values.loc[dmrs_dict[key],:]
    mean_dmr_df[key] = (np.mean(beta_key))
    # print("Finished", count, "/", len(EPIC_dmrs_dict))
mean_dmr_df.iloc[:]
print("")
print(mean_dmr_df)
mean_dmr_df.to_csv(base_dir + "Reports/Mean_DMR_Dataframe.csv")





# Plotting Each Individual Sample at sights with high blood and low sperm methylation.
if data_type == "EPIC":
    cutoffs = cutoffs_EPIC
if data_type == "450K":
    cutoffs = cutoffs_450K

# Figures are saved to the Figures Folder
print("")
print("Creating Contamination Figures for Each Sample")
print("")
count = 0
for sample in mean_dmr_df.index:
    count += 1
    sample_subset = mean_dmr_df.loc[sample,:]
    sample_subset = sample_subset.transpose()
    sample_subset = pd.DataFrame(sample_subset)
    plt.figure(figsize=(100,15))
    sns.barplot(data=cutoffs,x=cutoffs.index,y='Mean_of_betas_sperm', label='Mean Beta Value of all Sperm Samples',color = 'green', alpha = .5)
    sns.barplot(data=sample_subset,x=sample_subset.index,y=sample, color = 'red',label='Mean Beta Value for Individual Sample', alpha = .5)
    plt.legend(bbox_to_anchor=(1.005, 1), loc='upper left', borderaxespad=0,fontsize = 30)
    plt.title((sample),fontdict= {'fontsize': 50, 'fontweight':'bold','fontstyle':'italic','color':'black'},y =1.05)
    plt.ylabel("Mean Beta Value",fontdict= {'fontsize': 30, 'fontweight':'bold','fontstyle':'italic','color':'black'})
    plt.xlabel("Differentially Methylated Regions Between Blood and Sperm",fontdict= {'fontsize': 40, 'fontweight':'bold','fontstyle':'italic','color':'black'})
    plt.xticks(rotation=90,fontsize = 25)
    plt.yticks(size = 15)
    plt.ylim(0,0.35)
    plt.tight_layout()
    plt.savefig(base_dir + "Figures/" + sample + '.png')
    plt.clf()
    plt.close()
    print("Finished Creating Figure for Sample", count, "/", len(mean_dmr_df))





# Creating Dataframe that Includes Sample ID's, Data Type, # of DMRS analyzed, Contamination Scores, Contamination Calls, and Mean DLK1 Values
print("")
print("Generating Contamination Dataframe")
contamination_scores_df = pd.DataFrame(columns=['Sample_ID','Data_Type','Total_DMRS_Analyzed','Contamination_Score','Mean_DLK1','Contamination_Call'])

if data_type == "EPIC":
    cutoff = 40
    total_dmrs = 64
if data_type == "450K":
    cutoff = 25
    total_dmrs = 38

for sample in mean_dmr_df.index:
    count = 0
    mean_dlk1 = mean_dmr_df.loc[sample,"DLK1"]
    for region in mean_dmr_df.columns:
        if mean_dmr_df.loc[sample,region] > cutoffs.loc[region,"Mean_of_betas_sperm"]:
            count += 1
    if count >= cutoff and mean_dlk1 > .2:
        contamination_call = "Likely CONTAMINATED with Somatic Cells"
    else:
        contamination_call = "Likely NOT Contaminated with Somatic Cells"
    df2 = {'Sample_ID': sample, 'Data_Type': data_type, 'Total_DMRS_Analyzed': total_dmrs, 'Contamination_Score': count, 'Mean_DLK1': mean_dlk1, 'Contamination_Call': contamination_call}
    contamination_scores_df = contamination_scores_df.append(df2, ignore_index=True)
contamination_scores_df.index = contamination_scores_df["Sample_ID"]
del contamination_scores_df["Sample_ID"]
contamination_scores_df.to_csv(base_dir + "Reports/Contamination_Dataframe.csv")
contamination_scores_df.iloc[:]
print("")
print(contamination_scores_df)

print("")
print("Analysis Complete!")
print("")
print("All Figures and Reports Were Waved to", base_dir)
print("")