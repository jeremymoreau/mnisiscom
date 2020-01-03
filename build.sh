#!/bin/bash
# mnisiscom GUI Mac/Linux build script for pip and PyInstaller
# To be run in conda env with minimum dependencies installed
# Requires create-dmg (https://github.com/sindresorhus/create-dmg) for Mac build
version="0.4.0"

# Delete all files in dist and build folders
rm -r dist/*
rm -r build/*

# Build python wheel
python setup.py clean --all
python setup.py sdist bdist_wheel

# Re-install mnisiscom in env
pip install --upgrade --force-reinstall --no-deps dist/mnisiscom-*.whl

# PyInstaller build
python -m eel ./mnisiscom/mnisiscom.py ./mnisiscom/gui --paths ./mnisiscom/ --onefile --noconsole \
--add-data "./mnisiscom/MNI152_T1.nii:mnisiscom" --add-data "./mnisiscom/OpenSans-Regular.ttf:mnisiscom" \
--add-data "./LICENSE.md:mnisiscom" \
--add-data "$CONDA_PREFIX/lib/python3.7/site-packages/nilearn/plotting/glass_brain_files:nilearn/plotting/glass_brain_files" \
--hidden-import="sklearn.metrics.pairwise_fast" --hidden-import="sklearn.utils._cython_blas" \
--hidden-import="sklearn.neighbors.ball_tree" --hidden-import="sklearn.neighbors.typedefs" \
--hidden-import="sklearn.neighbors.quad_tree" --hidden-import="sklearn.tree" \
--hidden-import="sklearn.tree._utils" --icon ./icons/icon-gen/app.icns

# Create zip/dmg
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Change version number in Info.plist
    sed -i '' "s/0.0.0/$version/" dist/mnisiscom.app/Contents/Info.plist
    # Rename app
    mv dist/mnisiscom.app dist/MNI\ SISCOM.app
    # Create dmg
    create-dmg --overwrite dist/MNI\ SISCOM.app/ dist/
else
    zip -j dist/mniscom.zip  dist/mnisiscom README.md LICENSE.md
fi
