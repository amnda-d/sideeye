import os
from setuptools import setup, find_packages
from codecs import open

VERSION = "1.0.0a12"

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sideeye",
    version=VERSION,
    description="Library for analyzing eye-tracking-while-reading data",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/amnda-d/sideeye",
    project_urls={"Documentation": "https://sideeye.readthedocs.io/en/latest/"},
    author="Amanda Doucette",
    author_email="sideeye@amnda.me",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="eyetracking eye-tracking da1 psycholinguistics linguistics psychology eyetrack",
    python_requires=">=3.6",
    packages=find_packages(exclude=["doc", "tests"]),
    install_requires=["typing", "mypy", "mypy_extensions"],
    include_package_data=True,
    extras_require={"test": ["nose2", "pylint"], "dev": ["nose2", "pylint"]},
    package_data={"sideeye": ["default_config.json"]},
    test_suite="nose2.collector.collector",
    tests_require=["nose2", "pylint"],
    scripts=["bin/sideeye"],
)
