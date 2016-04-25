from django.test import TestCase
import unittest
from django.db import models
from .models import *

# Create your tests here.
class TestHomeworkquizModels(unittest.TestCase):
    
    #Testing the single choice answer model
    def test_singlechoice(self):
        test = SingleChoiceAnswer()
        test.answer = "test"
        return self.assertEqual(SingleChoiceAnswer.__str__(test), "test")


    #Testing the jax answer model
    def test_jaxanswer(self):
        test = JaxAnswer()
        test.answer = "testing qwerty"
        return self.assertEqual(JaxAnswer.__str__(test), "testing qwerty")
    
    #Testing the multiple choice answer model
    def test_multianswer(self):
        test = MultiChoiceAnswer()
        test.answer = "test \n +more test"
        return self.assertEqual(MultiChoiceAnswer.__str__(test), "test \n +more test")