from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
from PIL import _imagingft
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from dipy.align.reslice import reslice
from os.path import join
from contextlib import contextmanager
import subprocess
import nibabel as nib
import numpy as np
import brain_cmaps
import os
import platform
import sys
import gzip
import shutil
import pathlib
import contextlib
import warnings
with warnings.catch_warnings():  # ignore joblib DeprecationWarning caused by importing nilearn
    # TODO: Remove this when nilearn is updated
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    import sklearn
    from sklearn.neighbors.ball_tree import NeighborsHeap  # Only to prevent errors with PyInstaller
    from sklearn.neighbors import quad_tree  # Only to prevent errors with PyInstaller
import nilearn
from nilearn import masking
from nilearn import plotting


def ungzip(gzipped_file):
    """Un-gzip a gzipped file

    Parameters
    ----------
    gzipped_file : str
        Absolute path of a gzipped file

    Returns
    -------
    str
        Absolute path of ungzipped file
    """
    with gzip.open(gzipped_file, 'rb') as f_in:
        ungzipped_file = gzipped_file.split('.gz')[0]
        with open(ungzipped_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return ungzipped_file


def gzip_file(file_to_gzip):
    """gzip a file

    Parameters
    ----------
    file_to_gzip : str
        Absolute path of a gzipped file

    Returns
    -------
    str
        Absolute path of gzipped file
    """
    with open(file_to_gzip, 'rb') as f_in:
        gzipped_file = file_to_gzip + '.gz'
        with gzip.open(gzipped_file, 'wb') as f_out:
            f_out.writelines(f_in)

    return gzipped_file

            
def unzip_mac(zipped_file):
    """Un-zip a zipped file using Mac OS unzip command
    
    The Python zipfile module does not correctly extract aliases on Mac OS and
    does not preserve permissions. This function just calls the unzip command.
    
    Parameters
    ----------
    zipped_file : str
        Absolute path of a zipped file

    Returns
    -------
    str
        Absolute path of unzipped file
    """
    out_path = os.path.dirname(zipped_file)
    command = ['unzip', zipped_file, '-d', out_path]
    subprocess.run(command, stdout=subprocess.PIPE,
                    stdin=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    return out_path


def check_spm12app_mac(spm12_path):
    """Unzip spm12_maci64.zip if not already unzipped (only on Mac OS)
    
    Parameters
    ----------
    spm12_path : str
        Absolute path to run_spm12.sh
    """
    if platform.system() == 'Darwin':
        spm12_dir = os.path.dirname(spm12_path)
        spm12_app_dir = os.path.join(spm12_dir, 'spm12.app')
        spm12_app_zip = os.path.join(spm12_dir, 'spm12_maci64.zip')
        
        if not os.path.exists(spm12_app_dir) and os.path.isfile(spm12_app_zip):
            unzip_mac(spm12_app_zip)


def reslice_iso(orig_img):
    """Reslice nifti image into isotropic 1x1x1 space

    Parameters
    ----------
    img : nibabel.nifti1.Nifti1Image
        nibabel nii image object

    Returns
    -------
    nibabel.nifti1.Nifti1Image
        nibabel nii image object in 1x1x1 space

    """
    orig_data = orig_img.get_data()
    orig_affine = orig_img.affine
    orig_zooms = orig_img.header.get_zooms()[:3]
    new_zooms = (1., 1., 1.)
    new_data, new_affine = reslice(
        orig_data, orig_affine, orig_zooms, new_zooms)
    new_img = nib.Nifti1Image(new_data, new_affine)

    return new_img


def load_RAS_orient(path_to_nii):
    """Load nii and reorient to RAS orientation

    Parameters
    ----------
    path_to_nii : str
        Path to nii file

    Returns
    -------
    nibabel.nifti1.Nifti1Image
        nibabel nii image object in RAS orientation

    """
    nii = nib.load(path_to_nii)
    nii_RAS = nib.as_closest_canonical(nii)

    return nii_RAS


def run_cmd(command):
    """Wraps subprocess.run() to avoid console popping up on Windows with PyInstaller --noconsole

    Args:
        command (list): Liist of arguments to pass to subprocess.run()

    """
    if platform.system() == 'Windows':
        # Prevent PyInstaller executable from popping up a command window by default when
        # run with the --noconsole option.
        # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
        subprocess.run(command, startupinfo=si, env=env, stdout=subprocess.PIPE,
                        stdin=subprocess.DEVNULL, stderr=subprocess.PIPE)
    else:
        subprocess.run(command, stdout=subprocess.PIPE,
                        stdin=subprocess.DEVNULL, stderr=subprocess.PIPE)


def spm_coregister(target, sources, spm12_path, mcr_path):
    """Wraps SPM's spm.spatial.coreg

    Coregistered files are saved into the same dir as `target` and filename is prefixed with 'r'.

    Parameters
    ----------
    target : str
        Absolute path of target nii file
    sources : list of str
        Absolute paths of source nii files to coregister to target
    spm12_path : str
        Absolute path of SPM12 standalone binary (.sh or .exe)
    mcr_path : str
        Absolute path of Matlab Compiler Runtime (packaged with SPM12 standalone). May be an empty string on Windows systems.
    Returns
    -------
        None
    """
    # SPM batch script template
    spm_coreg_batch = """
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.ref = {{'{target}'}};
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.source = {{'{source}'}};
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.other = {{''}};
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.roptions.interp = 4;
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.roptions.mask = 0;
    matlabbatch{{1}}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';
    """

    if target.endswith('.gz'):
        target = ungzip(target)
    for i, source in enumerate(sources):
        if source.endswith('.gz'):
            source = ungzip(source)

        # Create SPM batch file
        spm_batch_file = os.path.join(os.path.dirname(
            target), 'spm_coregister_batch' + str(i) + '.m')
        with open(spm_batch_file, 'w') as batch_file:
            batch_file.write(spm_coreg_batch.format(
                target=target, source=source))

        # Run SPM batch file (Don't include MCR path if using Windows .exe)
        if spm12_path.endswith('.exe'):
            if os.path.isfile(spm12_path) and os.path.isfile(spm_batch_file):
                command = [spm12_path, 'batch', spm_batch_file]
        else:
            if os.path.isfile(spm12_path) and os.path.isdir(mcr_path) and os.path.isfile(spm_batch_file):
                command = [spm12_path, mcr_path, 'batch', spm_batch_file]
        
        # Unzip spm12_maci64.zip on Mac OS if user forgets
        check_spm12app_mac(spm12_path)
        
        # Change working dir to spm12_path before running command
        # This fixes an issue caused by a relative path in the spm12.app bundle on Mac OS
        cwd = os.getcwd()
        os.chdir(os.path.dirname(spm12_path))
        run_cmd(command)
        os.chdir(cwd)

        # remove SPM batch file
        os.remove(spm_batch_file)


def spm_normalise(source, apply_to, spm12_path, mcr_path):
    """Wraps SPM's spm.tools.oldnorm

    Normalised files are saved into the same dir as `source` and filename is prefixed with 'w'.

    Parameters
    ----------
    source : str
        Absolute path of nii file to use as source (e.g. a T1 MRI)
    apply_to : str
        Absolute path of nii files (that are already coregistered with the source nii) on which to apply the transformation
        from source -> MNI152
    spm12_path : str
        Absolute path of SPM12 standalone binary (.sh or .exe)
    mcr_path : str
        Absolute path of Matlab Compiler Runtime (packaged with SPM12 standalone). May be an empty string on Windows systems.
    Returns
    -------
        None
    """
    if getattr(sys, 'frozen', False):
        # Path for PyInstaller
        mni152_path = join(sys._MEIPASS, 'mnisiscom_data', 'MNI152_T1.nii')
    else:
        mni152_path = join(os.path.dirname(os.path.realpath(__file__)), 'MNI152_T1.nii')

    # SPM batch script template
    spm_norm_batch = """
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.subj.source = {{'{source},1'}};
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.subj.wtsrc = '';
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.subj.resample = {{'{apply_to},1'}};
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.template = {{'{mni152},1'}};
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.weight = '';
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.smosrc = 8;
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.smoref = 0;
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.regtype = 'mni';
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.cutoff = 25;
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.nits = 16;
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.eoptions.reg = 1;
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.roptions.preserve = 0;
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.roptions.bb = [-78 -112 -70
                                                            78 76 85];
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.roptions.vox = [2 2 2];
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.roptions.interp = 1;
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.roptions.wrap = [0 0 0];
    matlabbatch{{1}}.spm.tools.oldnorm.estwrite.roptions.prefix = 'w';
    """

    if source.endswith('.gz'):
        source = ungzip(source)

    if apply_to.endswith('.gz'):
        apply_to = ungzip(apply_to)

    # Create SPM batch file
    spm_batch_file = os.path.join(
        os.path.dirname(source), 'spm_normalise_batch.m')
    with open(spm_batch_file, 'w') as batch_file:
        batch_file.write(spm_norm_batch.format(
            source=source, apply_to=apply_to, mni152=mni152_path))

    # Run SPM batch file (Don't include MCR path if using Windows .exe)
    if spm12_path.endswith('.exe'):
        if os.path.isfile(spm12_path) and os.path.isfile(spm_batch_file):
            command = [spm12_path, 'batch', spm_batch_file]
    else:
        if os.path.isfile(spm12_path) and os.path.isdir(mcr_path) and os.path.isfile(spm_batch_file):
            command = [spm12_path, mcr_path, 'batch', spm_batch_file]
    
    # Unzip spm12_maci64.zip on Mac OS if user forgets
    check_spm12app_mac(spm12_path)
    
    # Change working dir to spm12_path before running command
    # This fixes an issue caused by a relative path in the spm12.app bundle on Mac OS
    cwd = os.getcwd()
    os.chdir(os.path.dirname(spm12_path))
    run_cmd(command)
    os.chdir(cwd)

    # Remove SPM batch file
    os.remove(spm_batch_file)
    
    # Remove SPM deformations files
    deformations_file = os.path.splitext(source)[0] + '_sn.mat'
    if os.path.isfile(deformations_file):
        os.remove(deformations_file)


def compute_siscom(interictal_nii, ictal_nii, out_dir, threshold=0.5, mask_cutoff=0.6):
    """Given coregistered interictal/ictal nii images, compute SISCOM

    Three files are created in out_dir:
        - ictal_z.nii.gz
        - interictal_z.nii.gz
        - siscom_z.nii.gz

    Parameters
    ----------
    interictal_nii : str
        Absolute path of interictal SPECT nii
    ictal_nii : str
        Absolute path of ictal SPECT nii
    out_dir : str
        Absolute path of dir in which to save result files
    threshold : float
        Threshold below which to zero out SISCOM result
    Returns
    -------
        None
    """
    # Load interictal and ictal image data
    interictal_img = load_RAS_orient(interictal_nii)
    interictal = interictal_img.get_data()
    ictal_img = load_RAS_orient(ictal_nii)
    ictal = ictal_img.get_data()

    # Get rid of pesky NaNs
    interictal[np.isnan(interictal)] = 0
    ictal[np.isnan(ictal)] = 0

    # Create a mask from interictal image and mask interictal/ictal images with it
    mask_img = masking.compute_epi_mask(
        interictal_img, lower_cutoff=mask_cutoff)
    mask = mask_img.get_data()
    ictal = ictal * mask
    interictal = interictal * mask

    # Compute z score of each image (individually)
    ictal_std = (ictal - np.mean(ictal)) / np.std(ictal)
    interictal_std = (interictal - np.mean(interictal)) / np.std(interictal)

    # Compute subtratction image
    siscom = ictal_std - interictal_std
    # siscom[siscom < 0] = 0  # ignore negative (i.e. where interictal > ictal)
    #siscom_std = (siscom - np.mean(siscom)) / np.std(siscom)

    # Threshold subtraction (ignore voxels where interictal > ictal)
    siscom[siscom < threshold] = 0

    # Save nifti
    new_img = nib.Nifti1Image(interictal_std, interictal_img.affine)
    new_img.to_filename(join(out_dir, 'interictal_z.nii.gz'))
    new_img = nib.Nifti1Image(ictal_std, ictal_img.affine)
    new_img.to_filename(join(out_dir, 'ictal_z.nii.gz'))
    new_img = nib.Nifti1Image(siscom, ictal_img.affine)
    new_img.to_filename(join(out_dir, 'siscom_z.nii.gz'))
    mask_img.to_filename(join(out_dir, 'interictal_mask.nii.gz'))


def get_slides_of_interest(mask_nii, slice_orientation):
    """Short summary.

    Parameters
    ----------
    mask_nii : str
        Absolute path of mask nii
    slice_orientation : str
        Either of 'ax', 'cor', or 'sag' for orientation in which to cut

    Returns
    -------
    min_slice : int
        index of min slice of interest
    max_slice : int
        index of max slice of interest

    """
    mask_data = reslice_iso(load_RAS_orient(mask_nii)).get_data()
    if slice_orientation == 'ax':
        nb_slices = mask_data.shape[2]
    elif slice_orientation == 'cor':
        nb_slices = mask_data.shape[1]
    elif slice_orientation == 'sag':
        nb_slices = mask_data.shape[0]
    else:
        raise ValueError(
            "Valid options for slice_orientation are 'ax', 'cor', or 'sag'")

    min_slice = 0
    max_slice = 0
    for i in range(nb_slices):
        if slice_orientation == 'ax':
            slice_avg = np.average(mask_data[:, :, i])
        elif slice_orientation == 'cor':
            slice_avg = np.average(mask_data[:, i, :])
        elif slice_orientation == 'sag':
            slice_avg = np.average(mask_data[i, :, :])
        if slice_avg > 0 and min_slice == 0:
            min_slice = i
        elif min_slice != 0 and slice_avg == 0 and max_slice == 0:
            max_slice = i - 1

    return min_slice, max_slice


def make_mri_panel(t1_nii, interictal_std_nii, ictal_std_nii, siscom_nii, mask_nii, out_dir,
                   slice_orientation='ax', slice_thickness=5, alpha=0.8, panel_type='all',
                   t1_window=(0.2, 0.9), spect_window=(0, 4.5), siscom_window=(0, 2)):
    """Plot a panel of MRI slices with SPECT results overlaid

    Parameters
    ----------
    t1_nii : str
        Absolute path of T1 nii
    interictal_std_nii : str
        Absolute path of interictal_std nii
    ictal_std_nii : str
        Absolute path of ictal_std nii
    siscom_nii : str
        Absolute path of SISCOM nii
    mask_nii : str
        Absolute path of mask nii
    out_dir : str
        Absolute path of dir in which to save result files
    slice_orientation : str
        Either of 'ax', 'cor', or 'sag' for orientation in which to cut
    slice_thickness : int
        Number of voxels in between slice snapshots
    alpha : float
        Value between 0 and 1 indicating the transparency of the overlay layer
    panel_type : str
        Either of 'all', 'mri_panel', or 'mri_slide', indicates the type of layout for output results
    t1_window : tuple of int or float
        Scaling factor for min and max values of T1 MRI (0 to 1)
    spect_window : tuple of int or float
        Min and max values for standardised SPECT images (standard deviations)
    siscom_window : tuple of int or float
        Min and max values for SISCOM image (difference of standard deviations)

    Returns
    -------
        None

    """
    # Load colour maps
    ge_cmap = brain_cmaps.ge_cmap()
    pet_cmap = brain_cmaps.pet_cmap()

    # Make results dirs
    results_dir = join(out_dir, 'SISCOM_results')
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)

    # Make slice snapshots
    # create dirs
    mri_panel_dir = join(results_dir, 'mri_panel')
    if not os.path.isdir(mri_panel_dir):
        os.mkdir(mri_panel_dir)
    dir_labels = ['interictal', 'ictal', 'siscom']
    for dir_label in dir_labels:
        dir_path = os.path.join(mri_panel_dir, dir_label)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    # load images
    t1_img = reslice_iso(load_RAS_orient(t1_nii))
    t1 = t1_img.get_data()
    t1 = np.squeeze(t1)
    interictal_std_img = reslice_iso(load_RAS_orient(interictal_std_nii))
    interictal_std = interictal_std_img.get_data()
    interictal_std = np.squeeze(interictal_std)
    ictal_std_img = reslice_iso(load_RAS_orient(ictal_std_nii))
    ictal_std = ictal_std_img.get_data()
    ictal_std = np.squeeze(ictal_std)
    siscom_img = reslice_iso(load_RAS_orient(siscom_nii))
    siscom = siscom_img.get_data()
    siscom = np.squeeze(siscom)
    images = [interictal_std, ictal_std, siscom]

    if slice_orientation == 'ax':
        nb_slices = ictal_std.shape[2]
        ax_slice1 = np.fliplr(t1[:, :, 1].T)
        xdim = ax_slice1.shape[0]
        ydim = ax_slice1.shape[1]
    elif slice_orientation == 'cor':
        nb_slices = ictal_std.shape[1]
        cor_slice1 = np.fliplr(t1[:, 1, :].T)
        xdim = cor_slice1.shape[0]
        ydim = cor_slice1.shape[1]
    elif slice_orientation == 'sag':
        nb_slices = ictal_std.shape[0]
        sag_slice1 = np.fliplr(t1[1, :, :].T)
        xdim = sag_slice1.shape[0]
        ydim = sag_slice1.shape[1]
    else:
        raise ValueError(
            "Valid options for slice_orientation are 'ax', 'cor', or 'sag'")

    # plot matplotlib figures
    dpi = 80  # This is to set fisize to actual pixel dimensions of image
    figsize = (ydim/dpi, xdim/dpi)

    min_slice, max_slice = get_slides_of_interest(mask_nii, slice_orientation)
    # ignore "too many figures" warning...
    plt.rcParams['figure.max_open_warning'] = 99999999
    for dir_label, image in zip(dir_labels, images):
        for s in range(nb_slices):
            if s % slice_thickness == 0 and s > min_slice and s < max_slice:
                fig = plt.figure(figsize=figsize, dpi=dpi)
                # plot T1 background (Flip LR for display in LAS radiological convetion)
                t1_min = (1 + t1_window[0]) * np.min(t1)
                t1_max = t1_window[1] * np.max(t1)
                if slice_orientation == 'ax':
                    fig.figimage(np.fliplr(
                        t1[:, :, s].T), origin='lower', cmap='gray', vmin=t1_min, vmax=t1_max)
                elif slice_orientation == 'cor':
                    fig.figimage(np.fliplr(
                        t1[:, s, :].T), origin='lower', cmap='gray', vmin=t1_min, vmax=t1_max)
                elif slice_orientation == 'sag':
                    fig.figimage(np.fliplr(
                        t1[s, :, :].T), origin='lower', cmap='gray', vmin=t1_min, vmax=t1_max)

                # plot overlay (Flip LR for display in LAS radiological convetion)
                if slice_orientation == 'ax':
                    slice_data = image[:, :, s].T
                elif slice_orientation == 'cor':
                    slice_data = image[:, s, :].T
                elif slice_orientation == 'sag':
                    slice_data = image[s, :, :].T
                if not dir_label == 'siscom':
                    fig.figimage(np.fliplr(slice_data), origin='lower', cmap=ge_cmap, alpha=alpha,
                                 vmin=spect_window[0], vmax=spect_window[1])
                else:
                    fig.figimage(np.fliplr(slice_data), origin='lower', cmap=pet_cmap, alpha=alpha,
                                 vmin=siscom_window[0], vmax=siscom_window[1])

                # save image
                filepath = join(mri_panel_dir, dir_label,
                                slice_orientation + str(s).zfill(4) + '.png')
                plt.savefig(filepath, bbox_inches='tight', pad_inches=0, dpi='figure',
                            transparent=False, facecolor='black')
                plt.close()

    # Get list of images for panels, and dimensions of a single image
    imagedirs = [join(mri_panel_dir, l) for l in dir_labels]
    imagefiles = []
    for imagedir in imagedirs:
        imagedir_images = [join(imagedir, i) for i in os.listdir(imagedir)]
        imagefiles = imagefiles + imagedir_images
    if slice_orientation == 'ax':
        imagefiles = [
            i for i in imagefiles if os.path.basename(i).startswith('ax')]
    elif slice_orientation == 'cor':
        imagefiles = [i for i in imagefiles if os.path.basename(
            i).startswith('cor')]
    elif slice_orientation == 'sag':
        imagefiles = [i for i in imagefiles if os.path.basename(
            i).startswith('sag')]

    first_image = Image.open(imagefiles[0])
    width = first_image.width
    height = first_image.height

    # Get font path
    if getattr(sys, 'frozen', False):
        # Path for PyInstaller
        font_path = join(sys._MEIPASS, 'mnisiscom_data', 'OpenSans-Regular.ttf')
    else:
        font_path = join(os.path.dirname(os.path.realpath(__file__)), 'OpenSans-Regular.ttf')

    # Check if panel type is valid
    if panel_type not in ['all', 'mri_panel', 'mri_slide']:
        raise ValueError(
            "Valid options for panel_type are 'all', 'mri_panel', or 'mri_slide'")
    # Assemble MRI panel
    if panel_type == 'all' or panel_type == 'mri_panel':
        columns = len(imagedirs)
        rows = len(imagefiles)//columns
        canvas_w = columns*width
        canvas_h = rows*height
        new_img = Image.new('RGB', (canvas_w, canvas_h))
        for i, dir_label in enumerate(dir_labels):
            images = [i for i in imagefiles if dir_label ==
                      pathlib.Path(i).parent.stem]
            images = sorted(images)
            for j, image in enumerate(images):
                img = Image.open(image)
                new_img.paste(img, (i*width, j*height))
        new_img_path = os.path.join(
            results_dir, 'SISCOM-' + slice_orientation + '_mri_panel.png')
        new_img.save(new_img_path)
        new_img.close()

        ## Add labels to MRI panel
        labels = ['Interictal', 'Ictal', 'SISCOM']
        img = Image.open(new_img_path)
        img = ImageOps.expand(img, border=30)
        panel_width, panel_height = img.size
        draw = ImageDraw.Draw(img)

        # Load font
        font = ImageFont.truetype(font_path, panel_width//30)

        # Draw labels
        uw = panel_width/100
        mult = panel_width / len(labels)  # i.e. panel width / 3
        for i, label in enumerate(labels):
            draw.text((i*mult + 2*uw, 3*uw), label, (255, 255, 255), font=font)
        # L/R labels (if ax or cor slices)
        if slice_orientation == 'ax' or slice_orientation == 'cor':
            draw.text((2*uw, 20*uw), 'R', (255, 255, 255), font=font)
            draw.text((panel_width - panel_width//30 - 2*uw, 20*uw), 'L', (255, 255, 255), font=font)
        img.save(new_img_path)
        img.close()

    # Assemble MRI slide
    if panel_type == 'all' or panel_type == 'mri_slide':
        for dir_label in dir_labels:
            images = [i for i in imagefiles if dir_label ==
                      pathlib.Path(i).parent.stem]
            images = sorted(images)
            nb_images = len(images)
            columns = 7
            rows = nb_images // columns
            # add an extra row for remainder images if neeeded
            if nb_images % columns != 0:
                rows += 1
            canvas_w = columns*width
            canvas_h = rows*height

            new_img = Image.new('RGB', (canvas_w, canvas_h))
            row_i = 0
            col_i = 0
            for i, image in enumerate(images):
                img = Image.open(image)
                new_img.paste(img, (col_i*width, row_i*height))
                if (i + 1) % columns == 0:
                    row_i += 1
                col_i += 1
                if col_i % columns == 0:
                    col_i = 0
            new_img_path = os.path.join(
                results_dir, dir_label.upper() + '-' + slice_orientation + '_mri_slide.png')
            new_img.save(new_img_path)
            new_img.close()

            ## Add L/R labels to MRI slide (only for ax or cor slides)
            if slice_orientation == 'ax' or slice_orientation == 'cor':
                img = Image.open(new_img_path)
                img = ImageOps.expand(img, border=30)
                panel_width, panel_height = img.size
                draw = ImageDraw.Draw(img)

                # Load font
                font = ImageFont.truetype(font_path, panel_width//30)

                # Draw L/R labels (radiological convention)
                uw = panel_width/100
                draw.text((2*uw, 2*uw), 'R', (255, 255, 255), font=font)
                draw.text((panel_width - panel_width//30 - 2*uw, 2*uw), 'L', (255, 255, 255), font=font)
                img.save(new_img_path)
                img.close()


def make_glass_brain(t1_nii, siscom_nii, out_dir, spm12_path, mcr_path):
    """Plot a glass brain view of the SISCOM results

    Spatially normalises images into MNI space using spm.Normalize() prior to plotting
    with nilearn.plotting.plot_glass_brain()

    Parameters
    ----------
    t1_nii : str
        Absolute path of T1 nii
    siscom_nii : str
        Absolute path of SISCOM result nii (registered with T1)
    out_dir : str
        Absolute path of dir in which to save result files
    spm12_path : str
        Absolute path of SPM12 standalone binary (.sh or .exe)
    mcr_path : str
        Absolute path of Matlab Compiler Runtime (packaged with SPM12 standalone). May be an empty string on Windows systems.
    Returns
    -------
        None

    """
    spm_normalise(t1_nii, siscom_nii, spm12_path, mcr_path)

    # Make results dirs
    results_dir = join(out_dir, 'SISCOM_results')
    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)

    # Plot glass brain
    with warnings.catch_warnings():
        # ignore scipy 'np.bool_' scalars... as index
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        plotting.plot_glass_brain(join(out_dir, join(out_dir, 'wsiscom_z.nii')),
                                  colorbar=True).savefig(join(results_dir, 'SISCOM-glass_brain.png'))


def create_output_dir(output_dir):
    siscom_dir = join(output_dir, 'SISCOM')
    file_suffix = 0
    while os.path.exists(siscom_dir):
        file_suffix += 1
        siscom_dir = join(output_dir, 'SISCOM' + str(file_suffix))
    if not os.path.exists(siscom_dir):
        os.mkdir(siscom_dir)

    return siscom_dir


def clean_output_dir(out_dir):
    # Remove unnecessary files
    unnecessary_files = ['ictal.nii', 'ictal.nii.gz', 'interictal.nii', 'interictal.nii.gz',
                         'T1_sn.mat', 'rictal.nii', 'siscom_z.nii']
    for unnecessary_file in unnecessary_files:
        if os.path.isfile(join(out_dir, unnecessary_file)):
            os.remove(join(out_dir, unnecessary_file))

    # Rename and gzip files
    files_to_rename = [
        ('rinterictal.nii', 'interictal_coregistered.nii'),
        ('rrictal.nii', 'ictal_coregistered.nii'),
        ('wsiscom_z.nii', 'siscom_z_MNI152.nii')
    ]

    for file_tuple in files_to_rename:
        if os.path.isfile(join(out_dir, file_tuple[0])):
            os.rename(join(out_dir, file_tuple[0]), join(
                out_dir, file_tuple[1]))
            gzip_file(join(out_dir, file_tuple[1]))
            os.remove(join(out_dir, file_tuple[1]))

    # Keep only T1.nii.gz (or gzip T1.nii)
    t1_nii = join(out_dir, 'T1.nii')
    t1_niigz = join(out_dir, 'T1.nii.gz')
    if os.path.isfile(t1_niigz) and os.path.isfile(t1_nii):
        os.remove(t1_nii)
    elif os.path.isfile(t1_nii):
        gzip_file(t1_nii)
        os.remove(t1_nii)
