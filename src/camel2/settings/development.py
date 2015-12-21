"""
Setting specific to running Camel in a development environment.
"""

try:
    from camel2.settings.base import *  # NOQA
except ImportError as e:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*s&_3f625j!3h#re=j+qcq(t*hmg3y_28!8-l-l650abr1*+_*'
