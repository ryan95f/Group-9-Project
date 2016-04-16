from django.test import TestCase
import unittest
from .models import *
# Create your tests here.
class TestUserModels(unittest.TestCase):
    
    def test_create_superuser(self):
        user = CamelUser(identifier="c1234567",
            first_name="bob",
            last_name="bobson",
            is_an_student=False,
            is_an_lecturer=False,
            email="bob@bobson.com",
            password="12345678")
        
        user.is_admin = True

        if self.assertEqual(user.get_full_name(), "c1234567 : bob bobson"):
            return self.assertEqual(user.is_admin, True)
        
        return False
    
    def test_create_student_user(self):
        user = CamelUser(identifier="c1234567",
            first_name="bob",
            last_name="bobson",
            is_an_student=True,
            is_an_lecturer=False,
            email="bob@bobson.com",
            password="12345678")
        

        if self.assertEqual(user.get_full_name(), "c1234567 : bob bobson"):
            return self.assertEqual(user.is_admin, False) & self.assertEqual(user.is_student, True) & self.assertEqual(user.is_teacher, False)
        
        return False
    
    
    def test_create_teacher_user(self):
        user = CamelUser(identifier="c1234567",
            first_name="bob",
            last_name="bobson",
            is_an_student=False,
            is_an_lecturer=True,
            email="bob@bobson.com",
            password="12345678")
        

        if self.assertEqual(user.get_full_name(), "c1234567 : bob bobson"):
            return self.assertEqual(user.is_admin, False) & self.assertEqual(user.is_student, False) & self.assertEqual(user.is_teacher, True)
        
        return False