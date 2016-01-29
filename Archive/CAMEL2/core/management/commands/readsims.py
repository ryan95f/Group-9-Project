# -*- coding: utf-8 -*-

'''
readsimss.py (camel/management)

imports users from SIMS csv file of students enrolled on a module
'''

import os, time, csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User

from core.models import Module

SIMS_ROOT  = getattr(settings, 'SIMS_ROOT')

class Command(BaseCommand):
    args = '<module_code, sims_data.csv>'
    help = 'input: csv file of students enrolled on a module (sims format)'

    def handle(self, *args, **options):     

        # usage
        if not args or len(args) < 2:
            print 'Usage: python manage.py readsims module_code student_details.csv'
            return

        # process arguments
        module_code = args[0]
        
        mods = Module.objects.filter(code=module_code)
        if not mods:
            print 'Module %s not in the database.' % module_code
            return
        
        csv_file_name = os.path.join(SIMS_ROOT, args[1])

        # csv reader
        with open(csv_file_name) as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None) # skip header row

            # iterate over students
            for row in reader: # list of strings
            
                # check that module code matches
                if row and row[4] == module_code:
            
                    # info
                    for col in (0,1,2,4,5,14):
                        print '{0:<10}'.format( row[col] ),
                    print ''
                    
                    # create user
                    u = User()
                    u.username      = row[0].split('/')[0]
                    u.last_name     = row[1]
                    u.first_name    = row[2]
                    u.email         = row[14]
                    u.save()
                    

