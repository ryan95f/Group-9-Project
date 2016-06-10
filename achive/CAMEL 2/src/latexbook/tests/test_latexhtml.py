"""Contains a bunch of unit-tests which will allow us to confirm that our LaTeX is correctly
formatted to HTML.

Check here for information on writing and running tests:
https://docs.python.org/3/library/unittest.html
https://docs.djangoproject.com/en/1.9/topics/testing/
"""

from django.test import TestCase

from ..latexparser.tests.config.experimental_nodebank import BOOKNODES


class TestLaTeXHTML(TestCase):
    """
    Tests our 'latex_html.py' - which handles the conversion between LaTeX and HTML.
    """

    def test_single_command(self):
        """Tests if a single command node can be successfully converted to HTML."""
        return False