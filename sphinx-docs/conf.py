# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add project root to path for autodoc
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'Jaon'
copyright = '2026, Jaon Project'
author = 'Jaon Project'
release = '0.1.0'
version = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Chinese language support
language = 'zh_CN'
html_search_language = 'zh'

# Source file suffixes
source_suffix = '.rst'
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_static_path = ['_static']
html_title = 'Jaon 编程语言文档'
html_short_title = 'Jaon'

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

# Custom CSS for Chinese fonts
html_css_files = [
    "custom.css",
]

# Logo and favicon
html_logo = "../assets/logo/jaon-social.png"
html_favicon = "../assets/logo/jaon-logo.ico"

# -- Intersphinx mapping -----------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Autodoc settings --------------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
