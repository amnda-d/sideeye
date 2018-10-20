import os
from setuptools import setup, find_packages
from setuptools.command.install import install
from codecs import open

VERSION = '1.0.0a6'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sideeye',
    version=VERSION,
    description='Library for analyzing eye-tracking-while-reading data',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/amnda-d/sideeye',
    project_urls={
        'Documentation': '',
    },
    author='Amanda Doucette',
    author_email='sideeye@amnda.me',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='eyetracking eye-tracking da1 psycholinguistics linguistics psychology eyetrack',

    python_requires='>=3.5',

    packages=find_packages(exclude=['doc', 'tests']),

    include_package_data=True,

    extras_require={
        'test': ['nose2'],
        'dev': ['nose2', 'pylint']
    },

    package_data={
        'sideeye': ['default_config.json'],
    }
)
