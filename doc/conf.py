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
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'Proteus'
copyright = '2023, Pablo R.'
author = 'Pablo R.'

# The full version, including alpha/beta/rc tags
release = '1.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# pip install sphinx sphinx_rtd_theme 
# alabaster is another possilibity
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

#By default, Sphinx ignores modules whose name starts with a double underscore (__), 
# as they are considered private modules. However, with this variable set to True,
# we tell Sphinx to include these modules in the documentation.
napoleon_include_private_with_doc = True

# If we want to show just the name of the class and not the full path we can use the following:
# add_module_names = False

# This will make sure that the names of the default values, such as Global Variables will
# be preserved in the documentation. This mean that if we have a variable that contains a
# string with the absolute path of a file, this won't be shown, just the name of the variable.
autodoc_preserve_defaults = True

# TODO After generating the documentation with make, I have to change the css a:visited{color:#9b59b6}
# to a:visited{color:#2980b9} 