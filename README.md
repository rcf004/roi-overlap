# ROI overlap tool
This tool is used to assess the overlap between fMRI images and a specified atlas.

Inputting a fMRI image (e.g. *.nii) alongside an atlas image in the same template space as the input will return a resulting .nii.gz file that contains only the overlapping template regions 
## Requirements
python >= 3.8
numpy
nibabel

additionally, this tool uses [AFNI's 3dresample tool](https://afni.nimh.nih.gov/pub/dist/doc/program_help/3dresample.html) and [FSL's fslmaths tool](https://open.win.ox.ac.uk/pages/fslcourse/practicals/intro3/index.html#:~:text=fslmaths,-fslmaths), so be sure those tools are available on your system.

I recommend setting up a virtual environment using the provided requirements.txt. 

General instructions using Anaconda:
```conda create --name nibabel-env --channel conda-forge --file requirements.txt```
Running the above will create an virtual environment with the required packages installed.
you can enter the virtual environment with:
```conda activate nibabel-env```


## Arguments and general usage
Positional arguments:
```
input:				Input image file to assess overlap with atlas.
```
non-positional arguments:
```
-h, --help:			Displays a help message.

-a ATLAS, --atlas ATLAS:	Path to atlas image file to compare, required.
-k KEY, --key KEY:		Path to atlas label file. Must be .csv formatted as
				`index, label` for each ROI in atlas, required.
-t THRESH, --thresh THRESH:	Threshold level for input image, everything below
				threshold will not be considered during overlap, required.
-p PERCENT, --percent PERCENT:	Percentage (1-100) of atlas ROI that must be overlapping
			        with input to be considered as valid output, required.
-o OUTPUT, --output OUTPUT:     Output prefix for file name.
				Image: [OUTPUT]_[PERCENT]_overlapping_ROI.nii.gz
				Text: [OUTPUT]_[PERCENT]_ROI_labels.txt, required.
```

example usage:
```
python get_ROI_overlap.py \
	-a test_atlas.nii.gz \
	-k test_labels.csv \
	-t 5.1 -p 80 \
	-o test \
	test_activation.nii
```

This would read `test_activation.nii` and assess overlap with `test_atlas.nii.gz`. The input file would be thresholded at `5.1`, so all values below will not be considered. Only ROIs that have an 80% or greater overlap with the input will be included in the output.

