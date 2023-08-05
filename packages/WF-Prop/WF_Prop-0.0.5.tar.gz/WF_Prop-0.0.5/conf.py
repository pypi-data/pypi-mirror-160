# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
#sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../../WaveFunctionPropagation'))


# -- Project information -----------------------------------------------------

project = 'Wave_Function_Propagation'
copyright = '2022, Yair&Nadav'
author = 'Yair&Nadav'

# The full version, including alpha/beta/rc tags
release = '0.2'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
import sphinx_rtd_theme

extensions = ['sphinx_rtd_theme',
              'sphinx.ext.napoleon',
              'sphinx.ext.duration',
              'sphinx.ext.doctest',
              'sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.autosummary',
              'sphinx.ext.intersphinx',
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

html_theme_options = {
    'globaltoc_collapse': False,
    'globaltoc_maxdepth': None,
}
numpydoc_validation_checks = {"all"}
napoleon_google_docstring = False
napoleon_use_rtype = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
autodoc_member_order = 'bysource'
