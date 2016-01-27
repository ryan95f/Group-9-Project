--
## CAMEL: CArdiff Mathematics E-Learning
--

### manage.py commands

##### $ python manage.py refresh MODULE_CODE --options
	Refresh the database (content) for module MODULE_CODE
	Options:
		-t:	write module doctree, text format to stdout
		-x: write module doctree, xml format to stdout
		-d: pretend write to database
		-commit: real write to database
		
##### $ python manage.py cohort MODULE-CODE ACADEMIC-YEAR 
	Cohort specified by MODULE_CODE and ACADEMIC_YEAR
	Looks for a file modulecode_academicyear.xls in the XLS_ROOT
	
##### $ python manage.py import-cohort modulecode-academicyear.xls
	Cohort specified by MODULE_CODE and ACADEMIC_YEAR
	Cohort needs to be defined initially by ma1500_1415.xls, containing just a list of students
	Can import and export
	e.g. ma1500_1415.xls contains 
		1. student id
		2. assessment 1 (mark inc binary)
		list of studentsRefresh the user-module (many-to-many) tables database (content) for module MODULE_CODE
	Options:
		-t:	write module doctree, text format to stdout
		-x: write module doctree, xml format to stdout
		-d: pretend write to database
		-commit: real write to database
		
