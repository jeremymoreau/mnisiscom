import os
import subprocess

# This example script shows how to run mnisiscom on a batch of
# T1/interictal/ictal .nii files.

# Folder structure:
# batch_dir contains one folder for each patient
# each patient folder contains 3 .nii files (e.g. T1.nii, interictal.nii, ictal.nii)
batch_dir = '/export02/data/jeremy/projects/mnisiscom/siscom_batch'


for pt in os.listdir(batch_dir):
    pt_dir = os.path.join(batch_dir, pt)

    # Get filename of T1/ictal/interictal .nii files by matching the end of the filenames
    # e.g. pt#####_T1_brain.nii
    t1_file = [x for x in os.listdir(pt_dir) if x.endswith('_T1_brain.nii')][0]
    interictal_file = [x for x in os.listdir(pt_dir) if x.endswith('_InterIctal_axial.nii')][0]
    ictal_file = [x for x in os.listdir(pt_dir) if x.endswith('_Ictal_axial.nii')][0]
    
    # Get full path of each file (e.g. /path/to/pt#####_T1_brain.nii)
    t1_path = os.path.join(pt_dir, t1_file)
    interictal_path = os.path.join(pt_dir, interictal_file) 
    ictal_path = os.path.join(pt_dir, ictal_file)

    # Run mnisiscom command line tool (with default parameters)
    command = ['mnisiscom', '-t1', t1_path, '-ii', interictal_path, '-i', ictal_path, '-o', pt_dir]
    subprocess.run(command)
    