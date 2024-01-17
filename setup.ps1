python -m pip install build
rm -Recurse -Force .\build
rm -Recurse -Force .\dist
python -m build
python -m pip install --upgrade .\dist\figuregen-1.1.0.tar.gz