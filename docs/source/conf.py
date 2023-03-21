import os
import sys

sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(1, os.path.abspath('../..'))
# sys.path.insert(2, os.path.abspath('../../opnsense_api'))
# sys.path.insert(5, os.path.abspath('../../opnsense_api/diagnostics'))
# sys.path.insert(4, os.path.abspath('../../opnsense_api/firewall'))
# sys.path.insert(3, os.path.abspath('../../opnsense_api/interfaces'))
# sys.path.insert(2, os.path.abspath('../../opnsense_api/routing'))
# sys.path.insert(1, os.path.abspath('../../opnsense_api/unbound'))

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

extensions = ["myst_parser", 'sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.coverage', 'sphinx.ext.autosummary']
autosummary_generate = True
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "logo": {
        "text": "Python-OPNsense",
    },
}

html_static_path = ['_static']

