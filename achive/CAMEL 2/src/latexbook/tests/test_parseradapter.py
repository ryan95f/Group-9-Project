"""Contains unit-tests regarding parseradapter.py.

Check here for information on writing and running tests:
https://docs.python.org/3/library/unittest.html
https://docs.djangoproject.com/en/1.9/topics/testing/
"""

from django.test import TestCase

# from ..latexparser.tests.config.experimental_nodebank import BOOKNODES


class TestParserAdapter(TestCase):
    """
    Tests the functionality of 'parseradapter.py'.

    parseradapter.py contains the function 'write_to_django_database'.
    This function is used to write Nodes from our parser into our database - it is the adapter between the parser and
    Django.
    """

    def test_xyz(self):
        """An example test method."""
        return False
