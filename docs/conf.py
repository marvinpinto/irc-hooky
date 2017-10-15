# -*- coding: utf-8 -*-

import sys
import os
import guzzle_sphinx_theme

extensions = [
    'guzzle_sphinx_theme',
]

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'
project = u'irc-hooky'
copyright = u'2016, Marvin Pinto'
author = u'Marvin Pinto'
version = u'0.1.1'
release = u'0.1.1'
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'guzzle_sphinx_theme'
html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme_options = {
    "project_nav_name": "irc-hooky",
    "google_analytics_account": os.getenv('GOOGLE_ANALYTICS_ID', "no-google-analytics"),
    "base_url": "https://disjoint.ca/projects/irc-hooky/",
}
html_favicon = '_static/images/favicon.ico'
html_static_path = ['_static']
