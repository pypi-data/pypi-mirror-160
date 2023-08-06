import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dylab",
    version="0.0.2",
    author="QF-group (AG Chomaz), Heidelberg university",
    author_email="gao@physi.uni-heidelberg.de",
    description="An internal toolbox package used for analyzation data of an ultracold atom experiment.",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.physi.uni-heidelberg.de/gao/dylab",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'lmfit',
        'laserbeamsize'
    ],
)
