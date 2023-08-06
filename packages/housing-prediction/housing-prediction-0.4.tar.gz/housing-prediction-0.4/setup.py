from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="housing-prediction",
    version="0.4",
    description=(
        "A module with scripts to download housing data, train machine learning models "
        "and analyze their performance"
    ),
    license="MIT",
    long_description=long_description,
    author="Rishitosh Kumar Singh",
    author_email="rishitosh.singh@tigeranalytics.com",
    url="https://github.com/rishitoshsingh-ta/mle-training",
    package_dir={"": "src"},
    packages=find_packages("src"),
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    package_data={"housing": ["*.cfg"]},
    install_requires=[
        "pandas>=1.4.2",
        "scikit-learn>=1.0.2",
        "numpy>=1.22.3",
        "mlflow",
    ],  # external packages as dependencies
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "housing = housing.main:run",
        ],
    },
)
