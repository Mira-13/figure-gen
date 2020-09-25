python -m pip install matplotlib python-pptx pyexr scipy opencv-python wheel
python setup.py sdist bdist_wheel
python -m pip install --upgrade --force-reinstall .\dist\figuregen-0.2-py3-none-any.whl