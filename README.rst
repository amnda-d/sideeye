========
SideEye
========
|circleci| |docs|

SideEye is still in beta! New features are in development, but if you find any bugs or have suggestions, `Open a GitHub issue <https://github.com/zediski/sideeye/issues/new/choose>`_ or email `sideeye@amnda.me <sideeye@amnda.me>`_.

SideEye is a Python package for processing eye tracking data that interfaces with EyeTrack and Experiment Builder.

It is meant to parse eye-tracking-while-reading data and calculate useful experimental measures. Currently, SideEye can only parse the .DA1 file format and some .ASC formats, but other formats will be added later. The goal is to parse all eye-tracking-while-reading data into a common format, and provide a consistent and accurate method for processing the data.

Documentation (currently incomplete, but more detail than provided here) can be found at `sideeye.readthedocs.io <http://sideeye.readthedocs.io/en/latest/index.html#>`_.

Refer to `examples/sample.py <examples/sample.py>`_ for an up-to-date sample script.

Installation
------------------

SideEye requires Python >= 3.6.

::

  pip install sideeye


.. |docs| image:: https://readthedocs.org/projects/sideeye/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://sideeye.readthedocs.io/en/latest/?badge=latest

.. |circleci| image:: https://circleci.com/gh/amnda-d/sideeye/tree/master.svg?style=shield
    :alt: Build Status
    :scale: 100%
    :target: https://circleci.com/gh/amnda-d/sideeye/tree/master
