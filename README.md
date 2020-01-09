# MNI SISCOM

<img src="https://raw.githubusercontent.com/jeremymoreau/mnisiscom/master/icons/icon-gen/favicon-120.png" align="left" height="110" width="110" hspace="10">

MNI SISCOM is a Windows/Mac/Linux desktop and command line application for computing Subtraction ictal single-photon emission CT coregistered to MRI (SISCOM). The underlying Python library that implements the functionality of MNI SISCOM is also available on PyPi. Please cite the following paper if you use MNI SISCOM in a paper: [reference to come].

## Screenshots

![meningioma.app](https://raw.githubusercontent.com/jeremymoreau/mnisiscom/master/icons/mnisiscom_screenshot.png)

## Usage

Input MRI and SPECT volumes in NIfTI (.nii) format are supported. If you have raw DICOM images you can use a tool like dcm2nii (now available with [MRIcroGL](https://www.nitrc.org/projects/mricrogl/)) to convert them to NIfTI format. Details about each parameter can be viewed by hovering over the label in the desktop app or via `mnisiscom --help` for the command line tool. Resulting images will be saved in the selected output folder.

### Basic command line tool usage:

`mnisiscom -t1 T1.nii -ii interictal_spect.nii -i ictal_spect.nii -o /path/to/output/folder`

You can also launch the Desktop GUI from the command line:
`mnisiscom_gui`

## Installation

### MNI SISCOM desktop app

Download MNI SISCOM: <https://github.com/jeremymoreau/mnisiscom/releases>

- Windows: Double click mnisiscom_setup.exe and follow the instructions.
- Mac: Double click mnisiscom.dmg and move mnisiscom.app to your Applications folder
  - If you get a notification that `"mnisiscom" can't be opened because it is from an unidentified developer`, right-click on the app and select `Open`, then click on the `Open` button.
- Linux: Double click on mnisiscom.
  - If this doesn't work, you may need to right-click mnisiscom -> select `Properties` -> then the `Permissions` tab, and check the `Allow executing file as program` box.

> **Note 1:** You **must also install [SPM12](https://www.fil.ion.ucl.ac.uk/spm/) standalone** to use MNI SISCOM (SPM is used for SPECT/MRI image coregistration). See below for installation instructions for [Windows](####Windows), [Mac](####Mac-OS), and [Linux](####Linux). Once installed, set the installation path of SPM in the settings menu of MNI SISCOM.

> **Note 2:** **[Google Chrome](https://www.google.com/chrome/) or Chromium is also required** to use the desktop app interface of MNI SISCOM.

### MNI SISCOM command line tool & Python module

If you would like to use the command-line version of mnisiscom or the Python module, you can also install MNI SISCOM from PyPi. If you do not have python 3 yet, the Anaconda Python distribution is recommended: <https://www.anaconda.com/distribution/#download-section>

To install mnisiscom simply run:
`pip install mnisiscom`

> **Note:** On Windows you may need to install Visual Studio C++. See this question for more information: <https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat>

## SPM12 Installation

The standalone version of [SPM12](https://www.fil.ion.ucl.ac.uk/spm/) is required for MNI SISCOM to run (it is used for SPECT and MRI image coregistration). For a more complete installation guide, see the SPM website: <https://en.wikibooks.org/wiki/SPM/Standalone>

### Windows

1. Download and install the Microsoft Visual C++ runtime components (`vcredist_x64.exe`) and the MATLAB Compiler Runtime (MCR) for SPM (`MCRInstaller.exe`)
<https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/win64/>

    - Note: If you are running an older (32 bit) version of Windows, download and install the files from this link instead: <https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/win32/>

2. Download the current version of SPM12 standalone (e.g. `spm12_r7487.zip`)
<https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/>

3. Unzip the downloaded file and move the `spm12` folder to where you would like to save it (e.g. in `C:\Users\YourUsername\spm12`)

4. Start SPM12 to verify that it is properly installed (SPM12 will also need to unpack some files the first time it is run). Reboot your computer first if you run into any errors.
    - Open the spm12 folder (e.g. in `C:\Users\YourUsername\spm12`) and double click on `spm12_win64.exe`

### Mac OS

1. Download and install the MATLAB Compiler Runtime (MCR) for SPM (`MCRInstaller.dmg`)
<https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/maci64/>

2. Download the current version of SPM12 standalone (e.g. `spm12_r7487.zip`)
<https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/>

3. Unzip the downloaded file and move the `spm12` folder to where you would like to save it (e.g. in `/Users/YourUsername/spm12`)

4. Unzip the `spm12_maci64.zip` file in the `spm12` folder

5. Start SPM12 to verify that it is properly installed (SPM12 will also need to unpack some files the first time it is run). Reboot your computer first if you run into any errors.
    - In your Applications folder go to `/Applications/Utilities` and open the Terminal app
    - Type in `cd /path/to/where/you/put/the/spm12/folder` (e.g. `cd /Users/YourUsername/spm12`)
    - Then enter `./run_spm12.sh /Applications/MATLAB/MATLAB_Compiler_Runtime/v713/`. Note: you may need to change `/Applications/MATLAB/MATLAB_Compiler_Runtime/v713/` if you installed the MATLAB Compiler Runtime in a different location in step 1.

### Linux

1. Download and install the MATLAB Compiler Runtime (MCR) for SPM (`MCRInstaller.bin`)
<https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/glnxa64/>
    - Note: If you are running a 32-bit Linux distro, download and install the file from this link instead: <https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/glnx86/>

2. Download the current version of SPM12 standalone (e.g. `spm12_r7487.zip`)
<https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/>

3. Unzip the downloaded file and move the `spm12` folder to where you would like to save it (e.g. in `/home/YourUsername/spm12`)

4. Start SPM12 to verify that it is properly installed (SPM12 will also need to unpack some files the first time it is run). Reboot your computer first if you run into any errors.
    - Open a terminal
    - Type in `cd /path/to/where/you/put/the/spm12/folder` (e.g. `cd /home/YourUsername/spm12`)
    - Then enter `./run_spm12.sh /usr/local/MATLAB/MATLAB_Compiler_Runtime/v713/`. Note: you may need to change `/usr/local/MATLAB/MATLAB_Compiler_Runtime/v713/` if you installed the MATLAB Compiler Runtime in a different location in step 1.

> **Note:** If you have trouble installing SPM12 or the Matlab MCR for any reason, you can try downloading one of the more recent SPM12 standalone releases from [here](https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/dev/). In which case, you will need to download and install the matching Matlab MCR from the [MathWorks website](https://www.mathworks.com/products/compiler/matlab-runtime.html) (e.g. if you download spm12_r7487_*_R2019b.zip, then download and install MCR version R2019b).
