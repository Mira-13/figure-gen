python -m pip install build
rm -Recurse -Force .\build
rm -Recurse -Force .\dist
python -m build
python -m pip install --upgrade .\dist\figuregen-1.0.1.tar.gz