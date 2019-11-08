import click
import importlib
import siscom
importlib.reload(siscom)
import sys
import os
from os.path import join
import shutil
from colorama import init, deinit
from colorama import Fore, Back, Style
from pathlib import Path
import json

def save_settings(spm12_path, mcr_path):
    settings = {'spm12_path': spm12_path, 'mcr_path': mcr_path}

    home_dir = str(Path.home())
    settings_dir = os.path.join(home_dir, '.mnisiscom')

    if not os.path.isdir(settings_dir):
        os.mkdir(settings_dir)

    settings_file = os.path.join(home_dir, '.mnisiscom', 'settings.json')

    with open(settings_file, 'w') as f:
        json.dump(settings, f)


def load_settings():
    home_dir = str(Path.home())
    settings_file = os.path.join(home_dir, '.mnisiscom', 'settings.json')

    if os.path.isfile(settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        if 'spm12_path' in settings and 'mcr_path' in settings:
            spm12_path = settings['spm12_path']
            mcr_path = settings['mcr_path']
            return (spm12_path, mcr_path)
        else:
            return ''
    else:
            return ''

@click.command()
@click.option('--t1', '-t1', type=click.Path(exists=True, dir_okay=False, resolve_path=True), required=True,
              help='T1 MRI NIfTI volume')
@click.option('--interictal', '-ii', type=click.Path(exists=True, dir_okay=False, resolve_path=True), required=True,
              help='Interictal SPECT NIfTI volume')
@click.option('--ictal', '-i', type=click.Path(exists=True, dir_okay=False, resolve_path=True), required=True,
              help='Ictal SPECT NIfTI volume')
@click.option('--out', '-o', type=click.Path(exists=True, file_okay=False, resolve_path=True), required=True,
              help='Directory in which to save SISCOM results')
@click.option('--siscom-threshold', type=float, default=0.5,
              help='Threshold value between 0 and 1 below which to zero out SISCOM results '
              '(i.e. Only display voxels where ictal (z-scored) - interictal (z-scored) > threshold). Default is 0.5')
@click.option('--mask-threshold', type=float, default=0.6,
              help='Threshold value between 0 and 1 for generating the interictal SPECT brain mask. Look at the '
                   '"interictal_mask.nii.gz" output file to judge the quality of the mask. Decrease the value '
                   'if the mask is too aggressive (i.e. cuts into brain parenchyma) and vice versa. Default is 0.6')
@click.option('--mripanel/--no-mripanel', default=True, help='Whether or not to plot SISCOM results as an MRI panel. '
              'Default is "--mripanel"')
@click.option('--mripanel-type', type=click.Choice(['all', 'panel', 'slide']), default='all',
              help='Type of MRI panel to save. The "panel" option saves a single image with three columns representing '
                   'interictal/ictal/SISCOM slices, the "slide" option saves a more compact image for each, and the '
                   '"all" option saves both. Default is "all"')
@click.option('--mripanel-orientation', type=click.Choice(['all', 'ax', 'cor', 'sag']), default='all',
              help='Orientation of slice cuts for MRI panel. Options are axial, coronal, sagittal, or all orientations.'
                   ' Default is "all"')
@click.option('--mripanel-thickness', type=int, default=5,
              help='Thickness of slices (in voxels) for MRI panel. Default is 5')
@click.option('--mripanel-transparency', type=float, default=0.8,
              help='Transparency value from 0 to 1 for interictal/ictal/SISCOM overlay layer. Default is 0.8 (80%)')
@click.option('--mripanel-t1window', type=(float, float), default=(0.2,0.9),
              help='Scaling factor for min and max values of T1 MRI (0 to 1). Default values are 0.1 0.9')
@click.option('--mripanel-spectwindow', type=(float, float), default=(0,4.5),
              help='Min and max values for standardised SPECT images (standard deviations). Default values are 0 4.5')
@click.option('--mripanel-siscomwindow', type=(float, float), default=(0,2),
              help='Min and max values for SISCOM image (difference of standard deviations). Default values are 0 2')
@click.option('--glassbrain/--no-glassbrain', default=True,
              help='Whether or not to plot SISCOM results as glass brain (MIP). Default is "--glassbrain"')
@click.option('--skipcoreg/--no-skipcoreg', default=False,
              help='Whether or not to skip the first coregistration step. Input images MUST already be coregistered and '
                   'have identical dimensions. Default is "--no-skipcoreg"')
def run_siscom(t1, interictal, ictal, out, siscom_threshold, mask_threshold,
                mripanel, mripanel_type, mripanel_orientation, mripanel_thickness,mripanel_transparency,
                mripanel_t1window, mripanel_spectwindow, mripanel_siscomwindow, glassbrain, skipcoreg):
    """
    Command line tool for computing subtraction ictal SPECT coregistered to MRI (SISCOM).\n
    For research use only!\n\n
    Author: Jeremy Moreau (jeremy.moreau@mail.mcgill.ca)\n
    Version: 0.3.1 (2019-07-14)
    """
    init()  # start colorama

    # Prompt for SPM12 standalone and MCR installation path if not already in settings
    settings = load_settings()
    if settings == '':
        if platform.system() == 'Windows':
            spm12_path = click.prompt('Enter the SPM12 standalone installation path (e.g. /path/to/spm12_win64.exe)', type=click.Path(exists=True))
            mcr_path = ''
        else:
            spm12_path = click.prompt('Enter the SPM12 standalone installation path (e.g. /path/to/run_spm12.sh)', type=click.Path(exists=True))
            mcr_path_message = """
            Enter the MATLAB Compiler Runtime installation path. The selected folder name should start with "v" (e.g. v95)
             and contain a subfolder called "mcr"
            """
            mcr_path = click.prompt(mcr_path_message, type=click.Path(exists=True))

        # Save settings
        save_settings(spm12_path, mcr_path)

    else:
        spm12_path = settings[0]
        mcr_path = settings[1]

    # Create output directory
    siscom_dir = join(out, 'SISCOM')
    file_suffix = 0
    while os.path.exists(siscom_dir):
        file_suffix += 1
        siscom_dir = join(out, 'SISCOM' + str(file_suffix))
    if not os.path.exists(siscom_dir):
        os.mkdir(siscom_dir)


    # Copy original T1, interictal, and ictal volumes to siscom_dir
    nii_basenames = []
    for nii in [t1, interictal, ictal]:
        shutil.copy2(nii, siscom_dir)
        nii_basenames.append(os.path.basename(nii))
    t1_nii = join(siscom_dir, nii_basenames[0])
    interictal_nii = join(siscom_dir, nii_basenames[1])
    ictal_nii = join(siscom_dir, nii_basenames[2])

    if not skipcoreg:
        # Coregister i/ii to t1, then coregister ri to rii (for better alignment)
        print(Fore.GREEN + 'Coregistering interictal/ictal SPECT images to T1 with SPM (~1-5 minutes)...')
        print(Style.RESET_ALL)
        siscom.spm_coregister(t1_nii, [interictal_nii, ictal_nii], spm12_path, mcr_path)
        rinterictal_nii = join(siscom_dir, 'r' + nii_basenames[1])
        rictal_nii = join(siscom_dir, 'r' + nii_basenames[2])
        siscom.spm_coregister(rinterictal_nii, [rictal_nii], spm12_path, mcr_path)
        rrictal_nii = join(siscom_dir, 'rr' + nii_basenames[2])
    else:
        rinterictal_nii = interictal_nii
        rrictal_nii = ictal_nii
        t1_nii = t1

    # Run SISCOM
    print(Fore.GREEN + 'Computing SISCOM images (~5-10s)...')
    print(Style.RESET_ALL)
    siscom.compute_siscom(rinterictal_nii, rrictal_nii, siscom_dir,
                          threshold=siscom_threshold, mask_cutoff=mask_threshold)

    # Get paths of result nii files
    interictal_z = join(siscom_dir, 'interictal_z.nii.gz')
    ictal_z = join(siscom_dir, 'ictal_z.nii.gz')
    siscom_z = join(siscom_dir, 'siscom_z.nii.gz')
    mask = join(siscom_dir, 'interictal_mask.nii.gz')

    # Make MRI panels
    if mripanel:
        print(Fore.GREEN + 'Plotting MRI panel results (~10-30s)...')
        print(Style.RESET_ALL)
        # Create list of slice orientations if 'all' option is selected
        if mripanel_orientation == 'all':
            panel_slices = ['ax', 'cor', 'sag']
        else:
            panel_slices = [mripanel_orientation]
        for panel_slice in panel_slices:
            siscom.make_mri_panel(t1_nii, interictal_z, ictal_z, siscom_z, mask, siscom_dir, slice_orientation=panel_slice,
                                  slice_thickness=mripanel_thickness, alpha=mripanel_transparency,
                                  panel_type=mripanel_type, t1_window=mripanel_t1window,
                                  spect_window=mripanel_spectwindow, siscom_window=mripanel_siscomwindow)

    # Make glass brain
    if glassbrain:
        print(Fore.GREEN + 'Plotting glass brain results (~30s-2 minutes)...')
        print(Style.RESET_ALL)
        siscom.make_glass_brain(t1_nii, siscom_z, siscom_dir, spm12_path, mcr_path)

    print(Fore.GREEN + 'Done!')
    print(Style.RESET_ALL)
    deinit()  # stop colorama


if __name__ == '__main__':
    run_siscom()
