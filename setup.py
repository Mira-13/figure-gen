import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='figuregen',
    version='1.3.2',
    description='Figure Generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Mira-13/figure-gen',
    author='Mira Niemann',
    author_email='mira.niemann@gmail.com',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        'matplotlib>=3.2.1',
        'python-pptx',
        'simpleimageio',
        'texsnip>=1.1.0'
    ],
    zip_safe=False,
    include_package_data=True
)
