import json
from colorama import Fore, Back, Style
from colorama import init, deinit
import shutil
from os.path import join
import os
import sys
import click
import platform
import importlib
from pathlib import Path
import siscom
importlib.reload(siscom)

license_text = """
Author: Jeremy Moreau
Copyright © 2020, McGill University

License Information
===================

MNI SISCOM is distributed under the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with your software, You can obtain one at https://mozilla.org/MPL/2.0/.

MNI SISCOM is also distributed under the terms of the following Healthcare Disclaimer.

Healthcare Disclaimer
---------------------
In Canada, the United States, or any other jurisdictions where they may apply, the following additional disclaimer of warranty and limitation of liability are hereby incorporated into the terms and conditions of MPL 2.0:

No warranties of any kind whatsoever are made as to the results that You will obtain from relying upon the covered code (or any information or content obtained by way of the covered code), including but not limited to compliance with privacy laws or regulations or clinical care industry standards and protocols. Use of the covered code is not a substitute for a health care provider’s standard practice or professional judgment. Any decision with regard to the appropriateness of treatment, or the validity or reliability of information or content made available by the covered code, is the sole responsibility of the health care provider. Consequently, it is incumbent upon each health care provider to verify all medical history and treatment plans with each patient.

Under no circumstances and under no legal theory, whether tort (including negligence), contract, or otherwise, shall any Contributor, or anyone who distributes Covered Software as permitted by the license, be liable to You for any indirect, special, incidental, consequential damages of any character including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other damages or losses, of any nature whatsoever (direct or otherwise) on account of or associated with the use or inability to use the covered content (including, without limitation, the use of information or content made available by the covered code, all documentation associated therewith, and the failure of the covered code to comply with privacy laws and regulations or clinical care industry standards and protocols), even if such party shall have been informed of the possibility of such damages.

License Information by [OpenMRS](https://openmrs.org/license) / [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)


OpenSans-Regular.ttf
====================
Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0)


MNI152_T1.nii
=============
Copyright (C) 1993–2009 Louis Collins, McConnell Brain Imaging Centre, Montreal Neurological Institute, McGill University. Permission to use, copy, modify, and distribute this software and its documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appear in all copies. The authors and McGill University make no representations about the suitability of this software for any purpose. It is provided “as is” without express or implied warranty. The authors are not responsible for any data loss, equipment damage, property loss, or injury to subjects or patients resulting from the use or misuse of this software package.
http://nist.mni.mcgill.ca/?page_id=714


Other licenses
==============
- [click](https://github.com/pallets/click) - [BSD-3-Clause](https://github.com/pallets/click/blob/master/LICENSE.rst)
- [colorama](https://github.com/tartley/colorama) - [BSD 3-Clause](https://github.com/tartley/colorama/blob/master/LICENSE.txt)
- [dipy](https://github.com/nipy/dipy) - [BSD 3-Clause](https://github.com/nipy/dipy/blob/master/LICENSE)
- [eel](https://github.com/samuelhwilliams/Eel) - [MIT License](https://github.com/samuelhwilliams/Eel/blob/master/LICENSE)
- [nibabel](https://github.com/nipy/nibabel) - [MIT License](https://github.com/nipy/nibabel/blob/master/COPYING)
- [numpy](https://github.com/numpy/numpy) - [BSD 3-Clause](https://github.com/numpy/numpy/blob/master/LICENSE.txt)
- [nilearn](https://github.com/nilearn/nilearn) - [New BSD License](https://github.com/nilearn/nilearn/blob/master/LICENSE)
- [matplotlib](https://github.com/matplotlib/matplotlib) - [Matplotlib License](https://github.com/matplotlib/matplotlib/blob/master/LICENSE/LICENSE)
- [Pillow](https://github.com/python-pillow/Pillow) - [PIL Software License](https://github.com/python-pillow/Pillow/blob/master/LICENSE)
- [scikit-learn](https://github.com/scikit-learn/scikit-learn) - [New BSD License](https://github.com/scikit-learn/scikit-learn/blob/master/COPYING)
- [argon](https://github.com/creativetimofficial/argon-design-system) - [MIT License](https://github.com/creativetimofficial/argon-design-system/blob/master/LICENSE.md)
- [bootstrap](https://github.com/twbs/bootstrap) - [MIT License](https://github.com/twbs/bootstrap/blob/master/LICENSE)
- [fontawesome](https://github.com/FortAwesome/Font-Awesome) - [Font Awesome Free License](https://github.com/FortAwesome/Font-Awesome/blob/master/LICENSE.txt)
- [jquery](https://github.com/jquery/jquery) - [MIT License](https://github.com/jquery/jquery/blob/master/LICENSE.txt) 
- [noUiSlider](https://github.com/leongersen/noUiSlider) - [MIT License](https://github.com/leongersen/noUiSlider/blob/master/LICENSE.md)
- [Popper.js](https://github.com/popperjs/popper.js) - [MIT License](https://github.com/popperjs/popper.js/blob/master/LICENSE.md)





Mozilla Public License Version 2.0
====================================


1. Definitions
-------------------

1.1. “Contributor”

means each individual or legal entity that creates, contributes to the creation of, or owns Covered Software.

1.2. “Contributor Version”

means the combination of the Contributions of others (if any) used by a Contributor and that particular Contributor’s Contribution.

1.3. “Contribution”

means Covered Software of a particular Contributor.

1.4. “Covered Software”

means Source Code Form to which the initial Contributor has attached the notice in Exhibit A, the Executable Form of such Source Code Form, and Modifications of such Source Code Form, in each case including portions thereof.

1.5. “Incompatible With Secondary Licenses”

means

1.  that the initial Contributor has attached the notice described in Exhibit B to the Covered Software; or

2.  that the Covered Software was made available under the terms of version 1.1 or earlier of the License, but not also under the terms of a Secondary License.


1.6. “Executable Form”

means any form of the work other than Source Code Form.

1.7. “Larger Work”

means a work that combines Covered Software with other material, in a separate file or files, that is not Covered Software.

1.8. “License”

means this document.

1.9. “Licensable”

means having the right to grant, to the maximum extent possible, whether at the time of the initial grant or subsequently, any and all of the rights conveyed by this License.

1.10. “Modifications”

means any of the following:

1.  any file in Source Code Form that results from an addition to, deletion from, or modification of the contents of Covered Software; or

2.  any new file in Source Code Form that contains any Covered Software.


1.11. “Patent Claims” of a Contributor

means any patent claim(s), including without limitation, method, process, and apparatus claims, in any patent Licensable by such Contributor that would be infringed, but for the grant of the License, by the making, using, selling, offering for sale, having made, import, or transfer of either its Contributions or its Contributor Version.

1.12. “Secondary License”

means either the GNU General Public License, Version 2.0, the GNU Lesser General Public License, Version 2.1, the GNU Affero General Public License, Version 3.0, or any later versions of those licenses.

1.13. “Source Code Form”

means the form of the work preferred for making modifications.

1.14. “You” (or “Your”)

means an individual or a legal entity exercising rights under this License. For legal entities, “You” includes any entity that controls, is controlled by, or is under common control with You. For purposes of this definition, “control” means (a) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (b) ownership of more than fifty percent (50%) of the outstanding shares or beneficial ownership of such entity.

2. License Grants and Conditions
---------------------------------

### 2.1. Grants

Each Contributor hereby grants You a world-wide, royalty-free, non-exclusive license:

1.  under intellectual property rights (other than patent or trademark) Licensable by such Contributor to use, reproduce, make available, modify, display, perform, distribute, and otherwise exploit its Contributions, either on an unmodified basis, with Modifications, or as part of a Larger Work; and

2.  under Patent Claims of such Contributor to make, use, sell, offer for sale, have made, import, and otherwise transfer either its Contributions or its Contributor Version.


### 2.2. Effective Date

The licenses granted in Section 2.1 with respect to any Contribution become effective for each Contribution on the date the Contributor first distributes such Contribution.

### 2.3. Limitations on Grant Scope

The licenses granted in this Section 2 are the only rights granted under this License. No additional rights or licenses will be implied from the distribution or licensing of Covered Software under this License. Notwithstanding Section 2.1(b) above, no patent license is granted by a Contributor:

1.  for any code that a Contributor has removed from Covered Software; or

2.  for infringements caused by: (i) Your and any other third party’s modifications of Covered Software, or (ii) the combination of its Contributions with other software (except as part of its Contributor Version); or

3.  under Patent Claims infringed by Covered Software in the absence of its Contributions.


This License does not grant any rights in the trademarks, service marks, or logos of any Contributor (except as may be necessary to comply with the notice requirements in Section 3.4).

### 2.4. Subsequent Licenses

No Contributor makes additional grants as a result of Your choice to distribute the Covered Software under a subsequent version of this License (see Section 10.2) or under the terms of a Secondary License (if permitted under the terms of Section 3.3).

### 2.5. Representation

Each Contributor represents that the Contributor believes its Contributions are its original creation(s) or it has sufficient rights to grant the rights to its Contributions conveyed by this License.

### 2.6. Fair Use

This License is not intended to limit any rights You have under applicable copyright doctrines of fair use, fair dealing, or other equivalents.

### 2.7. Conditions

Sections 3.1, 3.2, 3.3, and 3.4 are conditions of the licenses granted in Section 2.1.

3. Responsibilities
--------------------

### 3.1. Distribution of Source Form

All distribution of Covered Software in Source Code Form, including any Modifications that You create or to which You contribute, must be under the terms of this License. You must inform recipients that the Source Code Form of the Covered Software is governed by the terms of this License, and how they can obtain a copy of this License. You may not attempt to alter or restrict the recipients’ rights in the Source Code Form.

### 3.2. Distribution of Executable Form

If You distribute Covered Software in Executable Form then:

1.  such Covered Software must also be made available in Source Code Form, as described in Section 3.1, and You must inform recipients of the Executable Form how they can obtain a copy of such Source Code Form by reasonable means in a timely manner, at a charge no more than the cost of distribution to the recipient; and

2.  You may distribute such Executable Form under the terms of this License, or sublicense it under different terms, provided that the license for the Executable Form does not attempt to limit or alter the recipients’ rights in the Source Code Form under this License.


### 3.3. Distribution of a Larger Work

You may create and distribute a Larger Work under terms of Your choice, provided that You also comply with the requirements of this License for the Covered Software. If the Larger Work is a combination of Covered Software with a work governed by one or more Secondary Licenses, and the Covered Software is not Incompatible With Secondary Licenses, this License permits You to additionally distribute such Covered Software under the terms of such Secondary License(s), so that the recipient of the Larger Work may, at their option, further distribute the Covered Software under the terms of either this License or such Secondary License(s).

### 3.4. Notices

You may not remove or alter the substance of any license notices (including copyright notices, patent notices, disclaimers of warranty, or limitations of liability) contained within the Source Code Form of the Covered Software, except that You may alter any license notices to the extent required to remedy known factual inaccuracies.

### 3.5. Application of Additional Terms

You may choose to offer, and to charge a fee for, warranty, support, indemnity or liability obligations to one or more recipients of Covered Software. However, You may do so only on Your own behalf, and not on behalf of any Contributor. You must make it absolutely clear that any such warranty, support, indemnity, or liability obligation is offered by You alone, and You hereby agree to indemnify every Contributor for any liability incurred by such Contributor as a result of warranty, support, indemnity or liability terms You offer. You may include additional disclaimers of warranty and limitations of liability specific to any jurisdiction.

4. Inability to Comply Due to Statute or Regulation
----------------------------------------------------

If it is impossible for You to comply with any of the terms of this License with respect to some or all of the Covered Software due to statute, judicial order, or regulation then You must: (a) comply with the terms of this License to the maximum extent possible; and (b) describe the limitations and the code they affect. Such description must be placed in a text file included with all distributions of the Covered Software under this License. Except to the extent prohibited by statute or regulation, such description must be sufficiently detailed for a recipient of ordinary skill to be able to understand it.

5. Termination
---------------

5.1. The rights granted under this License will terminate automatically if You fail to comply with any of its terms. However, if You become compliant, then the rights granted under this License from a particular Contributor are reinstated (a) provisionally, unless and until such Contributor explicitly and finally terminates Your grants, and (b) on an ongoing basis, if such Contributor fails to notify You of the non-compliance by some reasonable means prior to 60 days after You have come back into compliance. Moreover, Your grants from a particular Contributor are reinstated on an ongoing basis if such Contributor notifies You of the non-compliance by some reasonable means, this is the first time You have received notice of non-compliance with this License from such Contributor, and You become compliant prior to 30 days after Your receipt of the notice.

5.2. If You initiate litigation against any entity by asserting a patent infringement claim (excluding declaratory judgment actions, counter-claims, and cross-claims) alleging that a Contributor Version directly or indirectly infringes any patent, then the rights granted to You by any and all Contributors for the Covered Software under Section 2.1 of this License shall terminate.

5.3. In the event of termination under Sections 5.1 or 5.2 above, all end user license agreements (excluding distributors and resellers) which have been validly granted by You or Your distributors under this License prior to termination shall survive termination.

6. Disclaimer of Warranty
--------------------------

_Covered Software is provided under this License on an “as is” basis, without warranty of any kind, either expressed, implied, or statutory, including, without limitation, warranties that the Covered Software is free of defects, merchantable, fit for a particular purpose or non-infringing. The entire risk as to the quality and performance of the Covered Software is with You. Should any Covered Software prove defective in any respect, You (not any Contributor) assume the cost of any necessary servicing, repair, or correction. This disclaimer of warranty constitutes an essential part of this License. No use of any Covered Software is authorized under this License except under this disclaimer._

7. Limitation of Liability
---------------------------

_Under no circumstances and under no legal theory, whether tort (including negligence), contract, or otherwise, shall any Contributor, or anyone who distributes Covered Software as permitted above, be liable to You for any direct, indirect, special, incidental, or consequential damages of any character including, without limitation, damages for lost profits, loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses, even if such party shall have been informed of the possibility of such damages. This limitation of liability shall not apply to liability for death or personal injury resulting from such party’s negligence to the extent applicable law prohibits such limitation. Some jurisdictions do not allow the exclusion or limitation of incidental or consequential damages, so this exclusion and limitation may not apply to You._

8. Litigation
--------------

Any litigation relating to this License may be brought only in the courts of a jurisdiction where the defendant maintains its principal place of business and such litigation shall be governed by laws of that jurisdiction, without reference to its conflict-of-law provisions. Nothing in this Section shall prevent a party’s ability to bring cross-claims or counter-claims.

9. Miscellaneous
-----------------

This License represents the complete agreement concerning the subject matter hereof. If any provision of this License is held to be unenforceable, such provision shall be reformed only to the extent necessary to make it enforceable. Any law or regulation which provides that the language of a contract shall be construed against the drafter shall not be used to construe this License against a Contributor.

10. Versions of the License
----------------------------

### 10.1. New Versions

Mozilla Foundation is the license steward. Except as provided in Section 10.3, no one other than the license steward has the right to modify or publish new versions of this License. Each version will be given a distinguishing version number.

### 10.2. Effect of New Versions

You may distribute the Covered Software under the terms of the version of the License under which You originally received the Covered Software, or under the terms of any subsequent version published by the license steward.

### 10.3. Modified Versions

If you create software not governed by this License, and you want to create a new license for such software, you may create and use a modified version of this License if you rename the license and remove any references to the name of the license steward (except to note that such modified license differs from this License).

### 10.4. Distributing Source Code Form that is Incompatible With Secondary Licenses

If You choose to distribute Source Code Form that is Incompatible With Secondary Licenses under the terms of this version of the License, the notice described in Exhibit B of this License must be attached.

Exhibit A - Source Code Form License Notice
-------------------------------------------

> This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.

If it is not possible or desirable to put the notice in a particular file, then You may include the notice in a location (such as a LICENSE file in a relevant directory) where a recipient would be likely to look for such a notice.

You may add additional accurate notices of copyright ownership.

Exhibit B - “Incompatible With Secondary Licenses” Notice
---------------------------------------------------------

> This Source Code Form is “Incompatible With Secondary Licenses”, as defined by the Mozilla Public License, v. 2.0.

"""


def save_settings(settings_dict):
    """Save settings dict to json file in home folder

    Settings will be saved in ~/.mnisiscom/settings.json 
    
    Args:
        settings_dict (dict): A dictionary of settings to save.
    """
    home_dir = str(Path.home())
    settings_dir = os.path.join(home_dir, '.mnisiscom')

    if not os.path.isdir(settings_dir):
        os.mkdir(settings_dir)

    settings_file = os.path.join(home_dir, '.mnisiscom', 'settings.json')

    with open(settings_file, 'w') as f:
        json.dump(settings_dict, f)


def load_settings():
    """Load seetings json file into a dict
    
    Settings will be loaded from ~/.mnisiscom/settings.json

    Returns:
        dict: A dictionary of settings for MNI SISCOM Returns an empty dict
              if no settings file exists.
    """
    home_dir = str(Path.home())
    settings_file = os.path.join(home_dir, '.mnisiscom', 'settings.json')

    if os.path.isfile(settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)
        return settings
    else:
        return {}


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
              '(i.e. only display voxels where ictal (z-scored) - interictal (z-scored) > threshold). Default is 0.5')
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
              help='Transparency value from 0 to 1 for interictal/ictal/SISCOM overlay layers. Default is 0.8 (80%)')
@click.option('--mripanel-t1window', type=(float, float), default=(0.2, 0.9),
              help='Scaling factor for min and max values of T1 MRI (0 to 1). Default values are 0.1 0.9')
@click.option('--mripanel-spectwindow', type=(float, float), default=(0, 4.5),
              help='Min and max values for standardised SPECT images (standard deviations). Default values are 0 4.5')
@click.option('--mripanel-siscomwindow', type=(float, float), default=(0, 2),
              help='Min and max values for SISCOM image (difference of standard deviations). Default values are 0 2')
@click.option('--glassbrain/--no-glassbrain', default=True,
              help='Whether or not to plot SISCOM results in a glass brain (MIP) view. This will also generate a SISCOM '
                   'results volume in standard MNI152 space, "siscom_z_MNI152.nii.gz". Default is "--glassbrain"')
@click.option('--skipcoreg/--no-skipcoreg', default=False,
              help='Whether or not to skip the first coregistration step. Input images MUST already be coregistered and '
                   'have identical dimensions. Default is "--no-skipcoreg"')
def run_siscom(t1, interictal, ictal, out, siscom_threshold, mask_threshold,
               mripanel, mripanel_type, mripanel_orientation, mripanel_thickness, mripanel_transparency,
               mripanel_t1window, mripanel_spectwindow, mripanel_siscomwindow, glassbrain, skipcoreg):
    """
    Command line tool for computing subtraction ictal SPECT coregistered to MRI (SISCOM).\n
    For research use only!\n\n
    Author: Jeremy Moreau (jeremy.moreau@mail.mcgill.ca)\n
    Version: 0.4.0 (2020-01-02)
    """
    init()  # start colorama

    ## Prompt for settings if not yet saved
    settings = load_settings()
    # Get user agreement
    if settings.get('agreed_to_license') == None or settings.get('agreed_to_license') == '':
        # prompt for acceptance
        accept = click.confirm(license_text + '\n I accept the agreement')
        if accept:
            settings['agreed_to_license'] = 'yes'
        else:
            print('You must agree to the license in order to use MNI SISCOM.')
            sys.exit(0)

    # Get SPM12 path
    if settings.get('spm12_path') == None or settings.get('spm12_path') == '':
        if platform.system() == 'Windows':
            spm12_path = click.prompt(
                '\nEnter the SPM12 standalone installation path (e.g. C:\\path\\to\\spm12_win64.exe)',
                type=click.Path(exists=True))
        else:
            spm12_path = click.prompt(
                '\nEnter the SPM12 standalone installation path (e.g. /path/to/run_spm12.sh)',
                type=click.Path(exists=True))
        settings['spm12_path'] = spm12_path
    else:
        spm12_path = settings['spm12_path']

    # Get MCR path (on Mac/Linux)
    if platform.system() != 'Windows':
        if settings.get('mcr_path') == None or settings.get('mcr_path') == '':
            mcr_path_message = '\nEnter the MATLAB Compiler Runtime installation path. The selected folder name should ' \
                               '\nstart with "v" (e.g. /path/to/v95) and contain a subfolder called "mcr"'
            mcr_path = click.prompt(
                mcr_path_message, type=click.Path(exists=True))
            settings['mcr_path'] = mcr_path
        else:
            mcr_path = settings['mcr_path']
    else:
        mcr_path = ''

    # Save settings
    save_settings(settings)


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
        siscom.spm_coregister(
            t1_nii, [interictal_nii, ictal_nii], spm12_path, mcr_path)
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
        print(Fore.GREEN + 'Plotting MRI panel results (~30s-1 minute)...')
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
        siscom.make_glass_brain(
            t1_nii, siscom_z, siscom_dir, spm12_path, mcr_path)

    # Clean output dir
    print(Fore.GREEN + 'Cleaning up result files... (~30s)')
    print(Style.RESET_ALL)
    siscom.clean_output_dir(siscom_dir)

    print(Fore.GREEN + 'Done!')
    print(Style.RESET_ALL)
    deinit()  # stop colorama


if __name__ == '__main__':
    run_siscom()
