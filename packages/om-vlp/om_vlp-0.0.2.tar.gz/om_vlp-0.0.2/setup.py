import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="om_vlp",
    packages = find_packages(),
    #packages = ["om_vlp"],
    #package_data={'om_vlp': ['*']},
    include_package_data=True,
    version="0.0.2",
    author="kyusonglee",
    description="VLP models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "mmcv",
        "timm",
        "torch",
        "torchvision"
    ]
)
