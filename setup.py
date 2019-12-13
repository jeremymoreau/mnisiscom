from setuptools import setup
from os import path

# Read the contents of README.md file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='mnisiscom',
      version='0.4.0',
      description='A simple command line tool and GUI for computing subtraction ictal SPECT coregistered to MRI (SISCOM). mnisiscom is exclusively intended for research use!',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords='neuroimaging spect mri siscom epilepsy radiology',
      url='https://github.com/jeremymoreau/mnisiscom',
      author='Jeremy Moreau',
      author_email='jeremy.moreau@mail.mcgill.ca',
      license='MPL 2.0 and Healthcare Disclaimer',
      classifiers=[
          'Intended Audience :: Science/Research',
              'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
              'Programming Language :: Python',
              'Programming Language :: JavaScript',
              'Topic :: Scientific/Engineering :: Medical Science Apps.',
              'Topic :: Scientific/Engineering',
              'Operating System :: POSIX :: Linux',
              'Operating System :: MacOS',
              'Operating System :: Microsoft :: Windows',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3.7',
      ],
      packages=['mnisiscom'],
      entry_points={
          'console_scripts': ['mnisiscom=mnisiscom.command_line:run_siscom',
                              'mnisiscom_gui=mnisiscom.mnisiscom:start_gui'],
      },
      include_package_data=True,
      python_requires='>=3.5, <3.8',
      install_requires=[
          'numpy',
          'nibabel',
          'scikit-learn',
          'nilearn',
          'dipy',
          'matplotlib',
          'Pillow',
          'click',
          'colorama',
          'eel',
          'pywin32 ; platform_system=="Windows"'
      ],
      zip_safe=False)
