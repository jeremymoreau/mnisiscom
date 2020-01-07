# mnisiscom GUI Windows build script for pip and PyInstaller
# To be run in conda env with minimum dependencies installed

# Delete all files in dist and build folders
Remove-Item .\dist\* -Recurse -Force
Remove-Item .\build\* -Recurse -Force

# Build python wheel
python setup.py clean --all
python setup.py sdist bdist_wheel

# Re-install mnisiscom in env
pip install --upgrade --force-reinstall --no-deps (Get-ChildItem .\dist\mnisiscom-*.whl | Select-Object -Expand FullName)

# PyInstaller build
pyinstaller .\mnisiscom\mnisiscom.py --paths .\mnisiscom\ `
--paths C:\Users\jerem\virtualenv\mnisiscom_distv\Lib\site-packages\scipy\.libs `
--paths C:\Users\jerem\virtualenv\mnisiscom_distv\Lib\site-packages\sklearn\.libs `
--noconsole  `
--add-data "$env:VIRTUAL_ENV\Lib\site-packages\eel\eel.js;eel" `
--add-data ".\mnisiscom\gui;mnisiscom_data\gui" `
--add-data ".\mnisiscom\MNI152_T1.nii;mnisiscom_data" `
--add-data ".\mnisiscom\OpenSans-Regular.ttf;mnisiscom_data" `
--add-data ".\LICENSE.md;mnisiscom_data" `
--add-data ".\README.md;mnisiscom_data" `
--add-data "$env:VIRTUAL_ENV\Lib\site-packages\nilearn\plotting\glass_brain_files;nilearn\plotting\glass_brain_files" `
--hidden-import="bottle_websocket" `
--hidden-import="sklearn.metrics.pairwise_fast" --hidden-import="sklearn.utils._cython_blas" `
--hidden-import="sklearn.neighbors.ball_tree" --hidden-import="sklearn.neighbors.typedefs" `
--hidden-import="sklearn.neighbors.quad_tree", --hidden-import="sklearn.tree" `
--hidden-import="sklearn.tree._utils" `
--icon .\icons\icon-gen\app.ico

# Convert LICENSE.md to .rtf for InnoSetup (requires pandoc)
pandoc -s .\LICENSE.md -o .\innosetup_license.rtf

# Build InnoSetup Installer (requires Inno Setup compiler)
iscc .\innosetup.iss

# Remove innosetup_license.rtf
Remove-Item .\innosetup_license.rtf