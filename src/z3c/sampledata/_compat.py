##############################################################################
#
# Copyright (c) 2005 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Compatibility between Python versions
"""
import base64
import sys

PY3 = sys.version_info[0] >= 3

if PY3:

    unicode = str
    basestring = str

    def toUnicode(obj):
        return obj.decode() if isinstance(obj, bytes) else str(obj)

else:

    unicode = toUnicode = unicode
    basestring = basestring
