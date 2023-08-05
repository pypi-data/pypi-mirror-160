"""
Type this in terminal to upgrade the package. (Write here for remember)
>> python setup.py sdist bdist_wheel
>> twine upload dist/*
"""
from setuptools import find_packages, setup

setup(name="handyscikit",
      version="0.0.4.1",
      description="VtkVisualize can show contour from mesh and result data.",
      author="Hong Peng",
      python_requires=">=3.7.0",
      url="https://github.com/minho-hong/handyscikit.git",
      packages=find_packages(),
      install_requires=["numpy", "vtk"],
      license="GPL")
