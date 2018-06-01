.. SideEye documentation master file, created by
   sphinx-quickstart on Mon Feb 19 14:35:27 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

SideEye
===================================

.. toctree::
   :maxdepth: 2
   :titlesonly:

   sideeye
   start
   configFile
   default_config.json
   changes

.. automodule:: sideeye

Introduction
============

SideEye is a Python package for processing data from eye-tracking while reading experiments. The package contains parsers that accept fixation data in .DA1 file format, and region definitions in several formats. SideEye calculates eye-tracking measures for parsed data, and can write output in .csv format.

Installation
------------------

SideEye requires Python >= 3.5.

::

  pip install sideeye
