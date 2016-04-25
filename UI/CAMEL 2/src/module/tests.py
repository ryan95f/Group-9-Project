from django.test import TestCase
from .models import *
import unittest
# Create your tests here.
class TestModuleModels(unittest.TestCase):
    
    def test_module(self):
        
        test = Module()
        test.code = "1234"
        test.year = "2014-15"
        test.title = "testmodule"
        
        return self.assertEqual(test.__str__(), "1234 - testmodule" )
    