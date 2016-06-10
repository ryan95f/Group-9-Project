from django.test import TestCase
import unittest
from django.db import models
from .models import *


class TestHomeworkquizModels(unittest.TestCase):
    """Unit test class for the module application"""
    def test_singlechoice(self):
        """Testing the single choice answer model"""
        test = SingleChoiceAnswer()
        test.answer = "test"
        return self.assertEqual(SingleChoiceAnswer.__str__(test), "test")

    def test_jaxanswer(self):
        """Testing the jax answer model"""
        test = JaxAnswer()
        test.answer = "testing qwerty"
        return self.assertEqual(JaxAnswer.__str__(test), "testing qwerty")

    def test_multianswer(self):
        """Testing the multiple choice answer model"""
        test = MultiChoiceAnswer()
        test.answer = "test \n +more test"
        return self.assertEqual(MultiChoiceAnswer.__str__(test), "test \n +more test")
