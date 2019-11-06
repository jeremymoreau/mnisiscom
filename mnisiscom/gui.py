import os
import platform
import random
import json
from pathlib import Path
from tkinter import Tk, filedialog

import eel

eel.init('gui')

@eel.expose
def get_nii_file():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file_path =  filedialog.askopenfilename(title = "Select file", filetypes=[("NIfTI Files", "*.nii")])
    
    return file_path

@eel.expose
def get_folder():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder_path = filedialog.askdirectory()
    
    return folder_path

@eel.expose
def get_spm_bin():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    spm12_path = ''
    if platform.system() == 'Windows':
        spm12_path =  filedialog.askopenfilename(title = "Select SPM12", filetypes=[("SPM12", "spm12_win64.exe")])
    else:
        spm12_path =  filedialog.askopenfilename(title = "Select SPM12", filetypes=[("SPM12", "run_spm12.sh")])

    
    return spm12_path

@eel.expose
def save_settings(spm12_path):
    settings = {'spm12_path': spm12_path}

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
        if 'spm12_path' in settings:
            spm12_path = settings['spm12_path']
            return spm12_path
        else:
            return 'no settings'
    else:
            return 'no settings'


eel.start('main.html', mode='chrome', size=(1000, 700))
