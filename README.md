
## Installation
### SPM12
The standalone version of [SPM12](https://www.fil.ion.ucl.ac.uk/spm/) is required for MNI SISCOM to run (it is used for SPECT and MRI image coregistration). For a more complete installation guide, see the SPM website: https://en.wikibooks.org/wiki/SPM/Standalone

#### Windows
1. Download and install the Microsoft Visual C++ runtime components (`vcredist_x64.exe`) and the MATLAB Compiler Runtime (MCR) for SPM (`MCRInstaller.exe`)
https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/win64/
    - Note: If you are running an older (32 bit) version of Windows, download and install the files from this link instead: https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/win32/

2. Download the current version of SPM12 standalone (e.g. `spm12_r7487.zip`)
https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/

3. Unzip the downloaded file and move the `spm12` folder to where you would like to save it (e.g. in `C:\Users\YourUsername\spm12`)

4. Start SPM12 to verify that it is properly installed (SPM12 will also need to unpack some files the first time it is run). Reboot your computer first if you run into any errors.
    - Open the spm12 folder (e.g. in `C:\Users\YourUsername\spm12`) and double click on `spm12_win64.exe`


#### Mac OS
1. Download and install the MATLAB Compiler Runtime (MCR) for SPM (`MCRInstaller.dmg`)
https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/maci64/

2. Download the current version of SPM12 standalone (e.g. `spm12_r7487.zip`)
https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/

3. Unzip the downloaded file and move the `spm12` folder to where you would like to save it (e.g. in `/Users/YourUsername/spm12`)

4. Unzip the `spm12_maci64.zip` file in the `spm12` folder

5. Start SPM12 to verify that it is properly installed (SPM12 will also need to unpack some files the first time it is run). Reboot your computer first if you run into any errors.
    - In your Applications folder go to `/Applications/Utilities` and open the Terminal app
    - Type in `cd /path/to/where/you/put/the/spm12/folder` (e.g. `cd /Users/YourUsername/spm12`)
    - Then enter `./run_spm12.sh /Applications/MATLAB/MATLAB_Compiler_Runtime/v713/`. Note: you may need to change `/Applications/MATLAB/MATLAB_Compiler_Runtime/v713/` if you installed the MATLAB Compiler Runtime in a different location in step 1.

#### Linux
1. Download and install the MATLAB Compiler Runtime (MCR) for SPM (`MCRInstaller.bin`)
https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/glnxa64/
    - Note: If you are running a 32-bit Linux distro, download and install the file from this link instead: https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/glnx86/

2. Download the current version of SPM12 standalone (e.g. `spm12_r7487.zip`)
https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/

3. Unzip the downloaded file and move the `spm12` folder to where you would like to save it (e.g. in `/home/YourUsername/spm12`)

4. Start SPM12 to verify that it is properly installed (SPM12 will also need to unpack some files the first time it is run). Reboot your computer first if you run into any errors.
    - Open a terminal
    - Type in `cd /path/to/where/you/put/the/spm12/folder` (e.g. `cd /home/YourUsername/spm12`)
    - Then enter `./run_spm12.sh /usr/local/MATLAB/MATLAB_Compiler_Runtime/v713/`. Note: you may need to change `/usr/local/MATLAB/MATLAB_Compiler_Runtime/v713/` if you installed the MATLAB Compiler Runtime in a different location in step 1.


### MNI SISCOM
Download MNI SISCOM: **link**
- Windows: Double click mnisiscom_setup.exe and follow the instructions.
- Mac: Double click mnisiscom.dmg and move mnisiscom.app to your Applications folder
    - If you get a notification that `"mnisiscom" can't be opened because it is from an unidentified developer`, right-click on the app and select `Open`, then click on the `Open` button.
- Linux: Double click on mnisiscom.
    - If this doesn't work, you may need to right-click mnisiscom -> select `Properties` -> then the `Permissions` tab, and check the `Allow executing file as program` box.

### MNI SISCOM Command line tool & Python module
If you would like to use the command-line version of mnisiscom or the Python module, you can also install MNI SISCOM from PyPi. If you do not have python 3 yet, the Anaconda Python distribution is recommended: https://www.anaconda.com/distribution/#download-section 

To install mnisiscom simply run:
`pip install mnisiscom`

You can then run the command line tool via a terminal:
`mnisiscom`

or open the Destop GUI:
`mnisiscom_gui`

For usage information, enter:
`mnisiscom --help`

Note: On Windows you may need to install Visual Studio C++. See this question for more information: https://stackoverflow.com/questions/29846087/microsoft-visual-c-14-0-is-required-unable-to-find-vcvarsall-bat
