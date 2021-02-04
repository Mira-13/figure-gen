python -m pip install wheel
python setup.py sdist bdist_wheel
python -m pip uninstall figuregen
python -m pip install --upgrade ./dist/figuregen-0.7.1-py3-none-any.whl
