import os
import platform
import random
import shutil
import subprocess
import sys
from os.path import join
from pathlib import Path
if not platform.system() == 'Darwin':
    from tkinter import Tk, filedialog

import eel
from colorama import Back, Fore, Style, deinit, init

import siscom


@eel.expose
def get_nii_file():
    # Use AppleScript instead of Tk filedialog on Mac
    # Tk filedialog is currently buggy on Mac OS
    if platform.system() == 'Darwin':
        ascript = 'tell application "SystemUIServer" to return POSIX path of (choose file with prompt "Choose a NIfTI (.nii) file" of type {"nii"})'
        raw_path = subprocess.run(['/usr/bin/osascript', '-e', ascript], capture_output=True)
        file_path = raw_path.stdout.decode('utf-8').rstrip()
    else:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        root.update()
        file_path = filedialog.askopenfilename(
            title="Select file", filetypes=[("NIfTI Files", "*.nii")], parent=root)
        root.update()
        root.destroy()

    return file_path


@eel.expose
def get_folder():
    # Use AppleScript instead of Tk filedialog on Mac
    # Tk filedialog is currently buggy on Mac OS
    if platform.system() == 'Darwin':
        ascript = 'tell application "SystemUIServer" to return POSIX path of (choose folder with prompt "Choose the output folder")'
        raw_path = subprocess.run(['/usr/bin/osascript', '-e', ascript], capture_output=True)
        folder_path = raw_path.stdout.decode('utf-8').rstrip()
    else:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        root.update()
        folder_path = filedialog.askdirectory(parent=root)
        root.update()
        root.destroy()

    return folder_path


@eel.expose
def get_mcr_folder():
    # Use AppleScript instead of Tk filedialog on Mac
    # Tk filedialog is currently buggy on Mac OS
    if platform.system() == 'Darwin':
        ascript = 'tell application "SystemUIServer" to return POSIX path of (choose folder with prompt "Select the MCR folder")'
        raw_path = subprocess.run(['/usr/bin/osascript', '-e', ascript], capture_output=True)
        folder_path = raw_path.stdout.decode('utf-8').rstrip()
    else:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        root.update()
        folder_path = filedialog.askdirectory()
        root.update()
        root.destroy()

    # Check if valid MCR folder is selected
    if os.path.isdir(folder_path):
        folder_content = os.listdir(folder_path)
        if 'bin' in folder_content:
            return folder_path
        else:
            return 'Invalid MCR folder.'
    else:
        return 'Invalid MCR folder.'


@eel.expose
def get_spm_bin():
    # Use AppleScript instead of Tk filedialog on Mac
    # Tk filedialog is currently buggy on Mac OS
    if platform.system() == 'Darwin':
        ascript = 'tell application "SystemUIServer" to return POSIX path of (choose file with prompt "Select SPM12 (run_spm12.sh)" of type {"sh"})'
        raw_path = subprocess.run(['/usr/bin/osascript', '-e', ascript], capture_output=True)
        spm12_path = raw_path.stdout.decode('utf-8').rstrip()
    else:
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        spm12_path = ''
        if platform.system() == 'Windows':
            root.update()
            spm12_path = filedialog.askopenfilename(title='Select SPM12 ("spm12_win64.exe")', filetypes=[
                                                    ("SPM12", "spm12_win64.exe")])
            root.update()
            root.destroy()
        else:
            # Linux
            root.update()
            spm12_path = filedialog.askopenfilename(
                title='Select SPM12 ("run_spm12.sh")', filetypes=[("SPM12", "run_spm12.sh")])
            root.update()
            root.destroy()

    return spm12_path


@eel.expose
def save_settings(settings_str):
    home_dir = str(Path.home())
    settings_dir = os.path.join(home_dir, '.mnisiscom')

    if not os.path.isdir(settings_dir):
        os.mkdir(settings_dir)

    settings_file = os.path.join(home_dir, '.mnisiscom', 'settings.json')

    with open(settings_file, 'w') as f:
        f.write(settings_str)


@eel.expose
def load_settings():
    home_dir = str(Path.home())
    settings_file = os.path.join(home_dir, '.mnisiscom', 'settings.json')

    if os.path.isfile(settings_file):
        with open(settings_file, 'r') as f:
            settings = f.read()
        return(settings)
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

    # Clean output dir
    eel.update_progress_bar('Cleaning up...', 90)
    print(Fore.GREEN + 'Cleaning up result files... (~30s)')
    print(Style.RESET_ALL)
    siscom.clean_output_dir(siscom_dir)
    deinit()  # stop colorama

    # Show done message in GUI
    eel.update_progress_bar('Done!', 100)
    eel.show_done_message()
    print(Fore.GREEN + 'Done!')
    print(Style.RESET_ALL)

    # Try opening the results folder (Check that dir exists before calling subprocess)
    if os.path.isdir(siscom_dir):
        if platform.system() == 'Windows':
            try:
                os.startfile(siscom_dir)
            except OSError:
                pass
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', siscom_dir],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            subprocess.Popen(['xdg-open', siscom_dir],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


def start_gui():
    """Start the mnisiscom GUI

    This function is used to start the mnisiscom GUI via the 'mnisiscom_gui' console_scripts entry point.

    """
    cwd = os.path.dirname(os.path.abspath(__file__))
    eel.init(join(cwd, 'gui'))
    eel.start('main.html', mode='chrome', size=(1000, 700), port=0)

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        # Path for PyInstaller
        eel.init(join('mnisiscom_data', 'gui'))
    else:
        # Path if started as script
        cwd = os.path.dirname(os.path.abspath(__file__))
        eel.init(join(cwd, 'gui'))
    eel.start('main.html', mode='chrome', size=(1000, 700), port=0)
