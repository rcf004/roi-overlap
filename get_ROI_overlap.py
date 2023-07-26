#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: robfren
"""

#%% imports

import os
import argparse
import subprocess
import numpy as np
import nibabel as nib

#%% create argparse object

parser = argparse.ArgumentParser(description="returns nii and text file of overlapping areas between input nii and specified atlas+key")
parser.add_argument("input", help="input image file to assess overlap with atlas")
parser.add_argument("-a", "--atlas", required=True,
                    help="path to atlas image file, must be in same space as input")
parser.add_argument("-k", "--key", required=True, 
                    help="path to atlas key, ie. what label is assigned to what index value in image.\n\tMust be .csv with index,label format.")
parser.add_argument("-t", "--thresh", required=True, type=float,
                    help="threshold where to binarise input image\n\tValues below will be 0, above will be 1")
parser.add_argument("-p", "--percent", required=True, type=int,
                    help="percentage (1-100) of atlas ROI that must overlap with input image before ROI is included")
parser.add_argument("-o", "--output", required=True, 
                    help="output file prefix for image file: '[output]_overlapping_ROI.nii.gz' and text file '[output]_ROI_labels.txt'")

args = parser.parse_args()

#%% error handling for input options

if args.percent<1 or args.percent>100:
    raise ValueError("-p/--percent must be an integer between 1-100")

#%% preparing input and atlas

# resample atlas to input space, ensures same voxel dimensions
afni_command = f"3dresample -input {args.atlas} -master {args.input} -prefix atlas_resample.nii.gz"
subprocess.run(afni_command, capture_output=False, text=True, shell=True) 

# binarising input image at specified threshold
fsl_command = f"fslmaths '{args.input}' -thr {args.thresh} -bin binarised_input.nii.gz"
subprocess.run(fsl_command, capture_output=False, text=True, shell=True) 

#%% load in data

loc = nib.load('./binarised_input.nii.gz')
loc_mat = loc.get_fdata()
sch = nib.load('./atlas_resample.nii.gz')
sch_mat = sch.get_fdata()

#%% 

# multiply two matrices (element-wise) to assess overlap
elem_prod = np.multiply(loc_mat, sch_mat)

sch_idx_keep = []

# iterate through parcels (only look at parcels in new map for efficiency)
for pnum in np.unique(elem_prod)[1:]:
    
    # get total vx count in parcellation and new masked product
    tot = np.count_nonzero(sch_mat == pnum)
    locnum = np.count_nonzero(elem_prod == pnum)
    
    # if proportion of voxels in masked product meets threshold keep the idx
    if locnum/tot*100 >= args.percent:
        sch_idx_keep.append(pnum)
        
# save these index numbers and also create a new parcellation nii with only these values.
full_labs = np.genfromtxt(f'./{args.key}', delimiter=',', dtype=str)

idx_nums = np.array(sch_idx_keep)-1
idx_nums = idx_nums.astype(int)

np.savetxt(f'./{args.output}_{args.percent}_ROI_labels.txt', full_labs[idx_nums,:], fmt='%s')
           
tom_loc_sch = np.where(np.isin(sch_mat,np.array(sch_idx_keep)), sch_mat, 0)

tom_loc_sch_nii = nib.Nifti1Image(tom_loc_sch, affine=sch.affine)
nib.save(tom_loc_sch_nii, f'./{args.output}_{args.percent}_overlapping_ROI.nii.gz')

# remove intermediate files
os.remove('./binarised_input.nii.gz')
os.remove('./atlas_resample.nii.gz')
