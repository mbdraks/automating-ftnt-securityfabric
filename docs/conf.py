# Project information
project = "Automation Guide to Fortinet Security Fabric"
copyright = "2020, Michel Barbosa"
author = "Michel Barbosa"
release = "1.0.0"


# Extensions
import sphinx_rtd_theme

extensions = [
    "sphinx_rtd_theme",
]

html_theme = "sphinx_rtd_theme"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_static_path = ["_static"]

# required to integrate with readthedocs.io
master_doc = "index"

# Custom

# Icon made by https://www.flaticon.com/authors/freepik
html_logo = "_static/img/logo.svg"
