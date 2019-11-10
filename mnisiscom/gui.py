import os
from os.path import join
import platform
import random
import json
import shutil
from pathlib import Path
from tkinter import Tk, filedialog
import siscom
from colorama import init, deinit
from colorama import Fore, Back, Style
import subprocess
import eel

eel.init('gui')


@eel.expose
def get_nii_file():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename(
        title="Select file", filetypes=[("NIfTI Files", "*.nii")])

    return file_path


@eel.expose
def get_folder():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder_path = filedialog.askdirectory()

    return folder_path


@eel.expose
def get_mcr_folder():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder_path = filedialog.askdirectory()

    # Check if valid MCR folder is selected
    folder_content = os.listdir(folder_path)
    if 'mcr' in folder_content:
        return folder_path
    else:
        return 'Invalid MCR folder.'


@eel.expose
def get_spm_bin():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    spm12_path = ''
    if platform.system() == 'Windows':
        spm12_path = filedialog.askopenfilename(title="Select SPM12", filetypes=[
                                                ("SPM12", "spm12_win64.exe")])
    else:
        spm12_path = filedialog.askopenfilename(
            title="Select SPM12", filetypes=[("SPM12", "run_spm12.sh")])

    return spm12_path


@eel.expose
def save_settings(spm12_path, mcr_path):
    settings = {'spm12_path': spm12_path, 'mcr_path': mcr_path}

    home_dir = str(Path.home())
    settings_dir = os.path.join(home_dir, '.mnisiscom')

    if not os.path.isdir(settings_dir):
        os.mkdir(settings_dir)

    settings_file = os.path.join(home_dir, '.mnisiscom', 'settings.json')

    with open(settings_file, 'w') as f:
        json.dump(settings, f)


@eel.expose
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


@eel.expose
def run_siscom(param_dict):
    init()  # start colorama

    # Get param values
    out = param_dict['output_path']
    t1 = param_dict['t1_mri_path']
    interictal = param_dict['interictal_spect_path']
    ictal = param_dict['ictal_spect_path']
    spm12_path = param_dict['spm12_path']
    mcr_path = param_dict['mcr_path']

    skipcoreg = param_dict['skip_coreg']
    mripanel = param_dict['mri_panel']
    glassbrain = param_dict['glass_brain']

    mripanel_t1window = tuple([float(x) for x in param_dict['mri_window']])
    mripanel_spectwindow = tuple([float(x)
                                  for x in param_dict['spect_window']])
    mripanel_siscomwindow = tuple([float(x)
                                   for x in param_dict['siscom_window']])

    mripanel_thickness = int(float(param_dict['slice_thickness']))
    mripanel_transparency = float(param_dict['overlay_transparency'])
    siscom_threshold = float(param_dict['siscom_threshold'])
    mask_threshold = float(param_dict['mask_threshold'])

    # Create output directory
    siscom_dir = siscom.create_output_dir(out)

    # Copy original T1, interictal, and ictal volumes to siscom_dir
    t1_nii = shutil.copy(
        t1, join(siscom_dir, 'T1' + ''.join(Path(t1).suffixes)))
    interictal_nii = shutil.copy(interictal, join(
        siscom_dir, 'interictal' + ''.join(Path(interictal).suffixes)))
    ictal_nii = shutil.copy(ictal, join(
        siscom_dir, 'ictal' + ''.join(Path(ictal).suffixes)))

    if not skipcoreg:
        # Coregister i/ii to t1, then coregister ri to rii (for better alignment)
        print(Fore.GREEN + 'Coregistering interictal/ictal SPECT images to T1 with SPM (~1-5 minutes)...')
        print(Style.RESET_ALL)

        eel.update_progress_bar('Coregistering images...', 0)
        siscom.spm_coregister(
            t1_nii, [interictal_nii, ictal_nii], spm12_path, mcr_path)

        eel.update_progress_bar('Coregistering images...', 20)
        rinterictal_nii = join(siscom_dir, 'rinterictal.nii')
        rictal_nii = join(siscom_dir, 'rictal.nii')
        siscom.spm_coregister(
            rinterictal_nii, [rictal_nii], spm12_path, mcr_path)

        rrictal_nii = join(siscom_dir, 'rrictal.nii')
    else:
        rinterictal_nii = interictal_nii
        rrictal_nii = ictal_nii
        t1_nii = t1

    # Run SISCOM
    eel.update_progress_bar('Computing SISCOM...', 40)
    print(Fore.GREEN + 'Computing SISCOM images (~5-30s)...')
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
        eel.update_progress_bar('Plotting MRI panel results...', 50)
        print(Fore.GREEN + 'Plotting MRI panel results (~30s-1 minute)...')
        print(Style.RESET_ALL)
        # Create list of slice orientations if 'all' option is selected
        panel_slices = ['ax', 'cor', 'sag']
        for panel_slice in panel_slices:
            siscom.make_mri_panel(t1_nii, interictal_z, ictal_z, siscom_z, mask, siscom_dir, slice_orientation=panel_slice,
                                  slice_thickness=mripanel_thickness, alpha=mripanel_transparency,
                                  panel_type='all', t1_window=mripanel_t1window,
                                  spect_window=mripanel_spectwindow, siscom_window=mripanel_siscomwindow)

    # Make glass brain
    if glassbrain:
        eel.update_progress_bar('Plotting glass brain results...', 70)
        print(Fore.GREEN + 'Plotting glass brain results (~30s-2 minutes)...')
        print(Style.RESET_ALL)
        siscom.make_glass_brain(
            t1_nii, siscom_z, siscom_dir, spm12_path, mcr_path)

    print(Fore.GREEN + 'Done!')
    print(Style.RESET_ALL)

    # Clean output dir
    eel.update_progress_bar('Cleaning up...', 90)
    print(Fore.GREEN + 'Cleaning up result files... (~30s)')
    print(Style.RESET_ALL)
    siscom.clean_output_dir(siscom_dir)
    deinit()  # stop colorama

    # Show done message in GUI
    eel.update_progress_bar('Done!', 100)
    eel.show_done_message()

    # Open results folder
    if platform.system() == 'Windows':
        os.startfile(siscom_dir)
    elif platform.system() == 'Darwin':
        subprocess.run(['open', siscom_dir])
    else:
        subprocess.run(['xdg-open', siscom_dir])


if __name__ == '__main__':
    eel.start('main.html', mode='chrome', size=(1000, 700))
