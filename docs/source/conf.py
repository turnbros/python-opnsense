<<<<<<< HEAD
import os
import sys

sys.path.insert(5, os.path.abspath('..'))
sys.path.insert(4, os.path.abspath('../..'))

=======
>>>>>>> ifalatik-feature/unittesting
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Python-OPNsense'
copyright = '2023, Turnbros'
author = 'Turnbros'
release = '1.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

<<<<<<< HEAD
extensions = [
    "myst_parser",
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.autosummary',
    'enum_tools.autoenum'
]
autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "logo": {
        "text": "Python-OPNsense",
    },
    "show_nav_level": 2
}

html_static_path = ['_static']

html_sidebars = {

    "primary_sidebar_end": ["sidebar-nav-bs", "sidebar-ethical-ads"],
}
=======
extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
>>>>>>> ifalatik-feature/unittesting
