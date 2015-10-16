"""
file: camel/apps.py
    startup script for camel server
"""
from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'camel'
    verbose_name = "Cardiff Maths eLearning"

    def ready(self):
        
        pass  # startup code here
        '''
        Not sure what goes here.
        '''