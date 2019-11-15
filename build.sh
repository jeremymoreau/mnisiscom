#!/bin/bash
# mnisiscom GUI Mac/Linux build script for pip and PyInstaller
# To be run in conda env with minimum dependencies installed
rm -r dist/*
python setup.py sdist bdist_wheel
pip install --upgrade --force-reinstall --no-deps dist/mnisiscom-*.whl
python -m eel ./mnisiscom/gui.py ./mnisiscom/gui --paths ./mnisiscom/ --onefile --noconsole \
--add-data "./mnisiscom/MNI152_T1.nii:mnisiscom" --add-data "./mnisiscom/OpenSans-Regular.ttf:mnisiscom" \
--add-data "$CONDA_PREFIX/lib/python3.7/site-packages/nilearn/plotting/glass_brain_files:nilearn/plotting/glass_brain_files" \
--hidden-import="sklearn.metrics.pairwise_fast" --hidden-import="sklearn.utils._cython_blas" \
--hidden-import="sklearn.neighbors.ball_tree" --hidden-import="sklearn.neighbors.typedefs" \
--hidden-import="sklearn.neighbors.quad_tree", --hidden-import="sklearn.tree" \
--hidden-import="sklearn.tree._utils" --icon ./icons/icon-gen/app.icns
