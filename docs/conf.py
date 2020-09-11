"""Sphinx configuration."""
from datetime import datetime


project = "Funk Lines"
author = "Federico Oberndorfer"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
