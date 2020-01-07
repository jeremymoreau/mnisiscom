#!/bin/bash
# mnisiscom GUI Mac build script for pip and PyInstaller
# To be run in virtualenv with minimum dependencies installed
# Requires create-dmg (https://github.com/sindresorhus/create-dmg) for Mac build
version="0.4.0"

# Use `brew intall libpng` to get correct version of lib (for Pillow)
export DYLD_LIBRARY_PATH=/usr/local/Cellar/libpng/1.6.37/lib/

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
--onefile --noconsole --exclude-module "tkinter" \
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
--hidden-import="sklearn.tree._utils" \
--add-binary="/usr/local/Cellar/libpng/1.6.37/lib/libpng16.16.dylib:." \
--icon ./icons/icon-gen/app.icns

# Create dmg
# Change version number in Info.plist
sed -i '' "s/0.0.0/$version/" dist/mnisiscom.app/Contents/Info.plist
# Rename app
mv dist/mnisiscom.app dist/MNI\ SISCOM.app
# Create dmg
create-dmg --overwrite dist/MNI\ SISCOM.app/ dist/
