from django.test import TestCase
from .models import Module
import unittest


class TestModuleModels(unittest.TestCase):
    """Unit test class for the module application"""

    def test_module(self):
        """Test to add a new module"""
        test = Module()
        test.code = "1234"
        test.year = "2014-15"
        test.title = "testmodule"

        return self.assertEqual(test.__str__(), "1234 - testmodule")
