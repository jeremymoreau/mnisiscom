#!/bin/bash
# mnisiscom GUI Linux build script for pip and PyInstaller
# To be run in virtualenv with minimum dependencies installed
version="0.4.0"
site_packages="/home/jmoreau/.local/lib/python3.6/site-packages"

# Delete all files in dist and build folders
rm -r dist/*
rm -r build/*

# Build python wheel
python3 setup.py clean --all
python3 setup.py sdist bdist_wheel

# Re-install mnisiscom in env
pip install --upgrade --force-reinstall --no-deps dist/mnisiscom-*.whl

# PyInstaller build
pyinstaller ./mnisiscom/mnisiscom.py --paths ./mnisiscom/ \
--onefile --noconsole \
--add-data "$site_packages/eel/eel.js:eel" \
--add-data "./mnisiscom/gui:mnisiscom_data/gui" \
--add-data "./mnisiscom/MNI152_T1.nii:mnisiscom_data" \
--add-data "./mnisiscom/OpenSans-Regular.ttf:mnisiscom_data" \
--add-data "./LICENSE.md:mnisiscom_data" \
--add-data "./README.md:mnisiscom_data" \
--add-data "$site_packages/nilearn/plotting/glass_brain_files:nilearn/plotting/glass_brain_files" \
--hidden-import="bottle_websocket" \
--hidden-import="PIL._imagingft" \
--hidden-import="sklearn.metrics.pairwise_fast" --hidden-import="sklearn.utils._cython_blas" \
--hidden-import="sklearn.neighbors.ball_tree" --hidden-import="sklearn.neighbors.typedefs" \
--hidden-import="sklearn.neighbors.quad_tree" --hidden-import="sklearn.tree" \
--hidden-import="sklearn.tree._utils" --icon ./icons/icon-gen/app.icns

# Create zip/dmg
zip -j dist/mniscom_$version.zip  dist/mnisiscom README.md LICENSE.md
