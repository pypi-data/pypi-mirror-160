# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
The main module of :ref:`voga`.

.. autosummary::
   :toctree:

    lib

"""

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="https://voga.lino-framework.org")
srcref_url = 'https://gitlab.com/lino-framework/voga/blob/master/%s'
# doc_trees = ['docs']
