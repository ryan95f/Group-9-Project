"""Contains a bunch of unit-tests which will allow us to confirm that we can safely read & write
LaTeX Nodes into our database.

Check here for information on writing and running tests:
https://docs.python.org/3/library/unittest.html
https://docs.djangoproject.com/en/1.9/topics/testing/
"""

from django.test import TestCase

from ..latexparser.tests.config.experimental_nodebank import BOOKNODES


class TestParserAdapter(TestCase):
    """
    Tests our 'parseradapter.py' the functionality involved with the reading
    and writing of LaTeX nodes into the database.
    """

    def test_XYZ(self):
        """ """
        return False