#!/bin/bash
# mnisiscom GUI Linux build script for pip and PyInstaller
# To be run in virtualenv with minimum dependencies installed
version="0.4.0"
VIRTUAL_ENV="/export02/data/jeremy/bin/virtualenv/mnisiscom_distv"

# Delete all files in dist and build folders
rm -r dist/*
rm -r build/*

# Build python wheel
python setup.py clean --all
python setup.py sdist bdist_wheel

# Re-install mnisiscom in env
pip install --upgrade --force-reinstall --no-deps dist/mnisiscom-*.whl

# PyInstaller build
pyinstaller ./mnisiscom/mnisiscom.py --paths ./mnisiscom/ \
--onefile --noconsole \
--add-data "$VIRTUAL_ENV/lib/python3.7/site-packages/eel/eel.js:eel" \
--add-data "./mnisiscom/gui:mnisiscom_data/gui" \
--add-data "./mnisiscom/MNI152_T1.nii:mnisiscom_data" \
--add-data "./mnisiscom/OpenSans-Regular.ttf:mnisiscom_data" \
--add-data "./LICENSE.md:mnisiscom_data" \
--add-data "./README.md:mnisiscom_data" \
--add-data "$VIRTUAL_ENV/lib/python3.7/site-packages/nilearn/plotting/glass_brain_files:nilearn/plotting/glass_brain_files" \
--hidden-import="bottle_websocket" \
--hidden-import="PIL._imagingft" \
--hidden-import="sklearn.metrics.pairwise_fast" --hidden-import="sklearn.utils._cython_blas" \
--hidden-import="sklearn.neighbors.ball_tree" --hidden-import="sklearn.neighbors.typedefs" \
--hidden-import="sklearn.neighbors.quad_tree" --hidden-import="sklearn.tree" \
--hidden-import="sklearn.tree._utils" --icon ./icons/icon-gen/app.icns

# Create zip/dmg
zip -j dist/mniscom_$version.zip  dist/mnisiscom README.md LICENSE.md
