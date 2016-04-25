from django.test import TestCase
import unittest
from .models import *
# Create your tests here.
class TestUserModels(unittest.TestCase):
    
    #test that superusers are created correctly
    def test_create_superuser(self):
        test = CamelUserManager()
        test.model = CamelUser
        user = test.create_superuser(identifier="c1234567",
            first_name="bob",
            last_name="bobson",
            email="bob@bobson.com",
            password="12345678")
        

        if self.assertEqual(user.get_full_name(), "c1234567 : bob bobson"):
            return self.assertEqual(user.is_admin, True)
        
        return False
    
    #test that students are created correctly
    def test_create_student_user(self):
        test = CamelUserManager()
        test.model = CamelUser
        user = test.create_student(identifier="c1234568",
            first_name="bob",
            last_name="bobson",
            email="bob@bobson.com",
            password="12345678")
        

        if self.assertEqual(user.get_full_name(), "c1234568 : bob bobson"):
            return self.assertEqual(user.is_admin, False) & self.assertEqual(user.is_student, True) & self.assertEqual(user.is_teacher, False)
        
        return False
    
    #test that teachers are created correctly
    def test_create_teacher_user(self):
        test = CamelUserManager()
        test.model = CamelUser
        user = test.create_lecturer(identifier="c1234569",
            first_name="bob",
            last_name="bobson",
            email="bob@bobson.com",
            password="12345678")
        

        if self.assertEqual(user.get_full_name(), "c1234569 : bob bobson"):
            return self.assertEqual(user.is_student, False) & self.assertEqual(user.is_teacher, True)
        
        
    def test_duplicate_indentifiers(self):
        test = CamelUserManager()
        test.model = CamelUser
        with self.failUnlessRaises(ValueError):
            test.create_lecturer(identifier="c1234569",
            first_name="bob",
            last_name="bobson",
            email="bob@bobson.com",
            password="12345678")
            
        

        