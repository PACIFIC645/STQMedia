# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Add the parent directory of both "stqmedia" and "stqpictures" to sys.path.
# Assuming "conf.py" is located in STQMEDIA/source.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stqmedia.settings")
django.setup()


project = 'STQMedia'
copyright = '2025, STQMedia_Africa'
author = 'STQMedia_Africa'

# -- General configuration ---------------------------------------------------
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

extensions = [
    'sphinx.ext.autodoc',    # Automatically document Python modules
    'sphinx.ext.napoleon',   # Support for Google-style docstrings
    'sphinx.ext.viewcode',    # Add links to highlighted source code
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = ['node_modules']

language = 'en'  # Use language codes (e.g., 'en' instead of 'English')

# -- HTML output options -----------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # Use ReadTheDocs theme for better readability
html_static_path = ['_static']
