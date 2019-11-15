# mnisiscom GUI Windows build script for pip and PyInstaller
# To be run in conda env with minimum dependencies installed
del dist\*.*
python setup.py sdist bdist_wheel
pip install --upgrade --force-reinstall --no-deps (Get-ChildItem .\dist\mnisiscom-*.whl | Select-Object -Expand FullName)
python -m eel .\mnisiscom\gui.py .\mnisiscom\gui --paths .\mnisiscom\ --onefile --noconsole `
--add-data ".\mnisiscom\MNI152_T1.nii;mnisiscom" --add-data ".\mnisiscom\OpenSans-Regular.ttf;mnisiscom" `
--add-data "$env:CONDA_PREFIX\Lib\site-packages\nilearn\plotting\glass_brain_files;nilearn\plotting\glass_brain_files" `
--hidden-import="sklearn.metrics.pairwise_fast" --hidden-import="sklearn.utils._cython_blas" `
--hidden-import="sklearn.neighbors.ball_tree" --hidden-import="sklearn.neighbors.typedefs" `
--hidden-import="sklearn.neighbors.quad_tree", --hidden-import="sklearn.tree" `
--hidden-import="sklearn.tree._utils" -i .\icons\icon-gen\app.ico
