python -m pip install build
rm -rf ./build
rm -rf ./dist
python -m build
python -m pip install --upgrade ./dist/figuregen-1.3.1-py3-none-any.whl