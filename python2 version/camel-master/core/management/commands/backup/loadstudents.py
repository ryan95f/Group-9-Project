# -*- coding: utf-8 -*-

'''
loadstutents.py (camel/management)

xlrd: cell types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
'''

import os, time, xlrd

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from django.contrib.auth.models import User
from core.models import Student

XLS_ROOT  = getattr(settings, 'XLS_ROOT')

col_studentno = 0
col_lastname = 1
col_firstname = 2
col_email = 14

class Command(BaseCommand):
	args = '<module_code, student_details.xlsx>'
	help = 'columns: student_number, surname, firstname, ...'

	def handle(self, *args, **options):		

		# process arguments
		module_code = args[0]
		wb_file = os.path.join(XLS_ROOT, args[1])

		# open workbook
		wb = xlrd.open_workbook(wb_file)

		# get first sheet
		ws = wb.sheet_by_index(0)
		
		# iterate over rows (ignore first)
		curr_row = 0	
		while curr_row < ws.nrows - 1:
			curr_row += 1
			if ws.cell_type(curr_row, 0) == 1:
				sid = ws.cell_value(curr_row, 0)
				u = User( username=sid )
				if ws.cell_type(curr_row, 1) == 1:
					u.last_name = ws.cell_value(curr_row, 1)
				if ws.cell_type(curr_row, 2) == 1:
					u.first_name = ws.cell_value(curr_row, 2)
				if ws.cell_type(curr_row, 3) == 1:
					u.email = ws.cell_value(curr_row, 3)
				u.save()
				s = Student( user=u )
				s.nickname = ws.cell_value(curr_row, 3)
				s.save()
		
