# -*- coding: utf-8 -*-
#
# script for updating pdf files
# update.py updates the database (from the doctree)
# This script *must* complete successfully (exit code 0) before running update.py 
# so that we can be sure that main.tex at least compiles under latex
import os, re, time, shutil, logging, subprocess

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

SITE_ROOT = getattr(settings, 'SITE_ROOT')
TEX_ROOT  = getattr(settings, 'TEX_ROOT')

out = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<module_code, module_code, ...>'
    help = 'Updates pdf for module list'

    def handle(self, *args, **options): 	
		
		# info
		out.info('SITE_ROOT = %s' % SITE_ROOT)        
		out.info('TEX_ROOT  = %s' % TEX_ROOT)
		
		# initialise null device
		devnull = open(os.devnull, "w")
		
		# process argument (module code)
		# usage: $python manage.py makepdf MA2500
		
		for module_code in args:
			out.info('BEGIN processing %s', module_code)
			
			# find main.tex
			tex_file = os.path.join(TEX_ROOT, module_code, 'main.tex')

			# change to directory containing main.tex
			parent_dir = os.path.dirname(tex_file)
			os.chdir(parent_dir)
			pdf_dir = os.path.join(parent_dir, 'pdf')
			if not os.path.exists(pdf_dir):
				os.makedirs(pdf_dir)

			# construct file names
			base_name = os.path.splitext(tex_file)[0]
			raw_name = os.path.split(base_name)[1]
			pdf_file = os.path.join(base_name + '.pdf')
			# out.info('raw name = %s' % raw_name)

			# check "last modified" 
			if os.path.exists(pdf_file) and os.path.getmtime(pdf_file) > os.path.getmtime(tex_file):
				out.info('PDF up-to-date: %s', pdf_file)
				return
			else
				out.info('PDF update required: %s', pdf_file)
		
			# extract and check document attributes
			code, year = extract_document_attributes(tex_file)
			if not code or not year:
				out.warning('Mandatory attributes not set in %s', tex_file)
				return
			if code != module_code:
				out.warning('Module code does not match (%s)!', tex_file)
				return
			
			# paper version
			if texify(tex_file): 
				continue
			else:
				if os.path.exists(pdf_file):
					out_file = os.path.join(pdf_dir, raw_name + '-complete.pdf')
					shutil.copy(pdf_file, out_file)
				
					twoup_file = os.path.join(pdf_dir, raw_name + '-complete-1x2.pdf')
					cmd_line = 'pdfnup --column true --no-landscape --nup 1x2 --outfile ' + twoup_file + ' --quiet ' + out_file
					subprocess.call(cmd_line, shell=True, stdout=devnull)
				
					fourup_file = os.path.join(pdf_dir, raw_name + '-complete-2x2.pdf')
					cmd_line = 'pdfnup --column true --nup 2x2 --outfile ' + fourup_file + ' --quiet ' + out_file
					subprocess.call(cmd_line, shell=True, stdout=devnull)
		
			# blanks version
			if texify(tex_file, blanks=True): 
				continue
			else:
				if os.path.exists(pdf_file):
					out_file = os.path.join(pdf_dir, raw_name + '-with-blanks.pdf')
					shutil.copy(pdf_file, out_file)
				
					twoup_file = os.path.join(pdf_dir, raw_name + '-with-blanks-1x2.pdf')
					cmd_line = 'pdfnup --column true --no-landscape --nup 1x2 --outfile ' + twoup_file + ' --quiet ' + out_file
					subprocess.call(cmd_line, shell=True, stdout=devnull)
				
					fourup_file = os.path.join(pdf_dir, raw_name + '-with-blanks-2x2.pdf')
					cmd_line = 'pdfnup --column true --nup 2x2 --outfile ' + fourup_file + ' --quiet ' + out_file
					subprocess.call(cmd_line, shell=True, stdout=devnull)

			# end 
			out.info('END processing %s', module_code)

		# info
		devnull.close()
		timestr = time.strftime("%Y.%m.%d.%H.%M.%S")
		out.info('Logging ended at %s', timestr)


#------------------------------------------------
# texify
def texify(tex_file, screen=False, cymraeg=False, solutions=False, blanks=False):

	# process options
	opt_str = r'"'
	opt_str += r'Y\n' if cymraeg else r'N\n'
	opt_str += r'Y\n' if answers else r'N\n'
	opt_str += r'Y\n' if screen  else r'N\n'
	opt_str += r'Y\n' if blanks  else r'N\n'
	opt_str += r'"'

	# run latex
	cmd_line = ['echo -e', opt_str, '|', 'pdflatex', '-interaction=scrollmode', tex_file , '>/dev/null']
	cmd = ' '.join(cmd_line)
	return_value = os.system(cmd)
	if return_value:
		out.warning('Latex errors in file %s', tex_file)
		return return_value
	else:
		out.info('Latex OK: %s', tex_file)

	# run latex until xrefs sorted
	os.system(cmd)
	os.system(cmd)
	
	# clean up
	base_name = os.path.splitext(tex_file)[0]
	for ext in ['.aux','.log','.out','.thm','.toc','.ans']:
		aux_file = base_name + ext
		if os.path.exists(aux_file): 
			os.remove(aux_file)
	
	# close null device
	devnull.close()
	return 0	

#------------------------------------------------
def extract_document_attributes(tex_file):

	# initialise return values
	module_code = None
	academic_year = None

	# open file
	try:
		f = open(tex_file, 'r')
	except IOError:
		out.warning('Failed to open %s', tex_file)
		return (None, None)

	s = f.read()
	f.close()

	# extract module code
	match = re.compile(r'\\modulecode\{(\w+)\}').search(s)
	if match: 
		module_code = match.groups()[0]
	else:
		out.warning('module_code not specified in file %s', tex_file)

	# extract academic year
	match = re.compile(r'\\academicyear\{(.*)\}').search(s)
	if match:
		'academic_year' = match.groups()[0]
	else:
		out.warning('acedemic_year not specified in  file %s', tex_file)

	# end
	return (module_code, academic_year)

#------------------------------------------------
# extract class options
def extract_class_options(tex_file):
	
	try:
		f = open(tex_file, 'r')
	except IOError:
		out.warning('Failed to open %s', tex_file)
		return None

	s = f.read()
	f.close()
	match = re.compile(r'\\documentclass\[(.*)\]\{(.*)\}').search(s)
	if match:
		options = m.groups()[0].split(',')
		options = [options[idx].strip() for idx in range(len(options))]
		return options
	else:
		return None


