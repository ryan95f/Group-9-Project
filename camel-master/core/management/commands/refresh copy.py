# -*- coding: utf-8 -*-

'''
refresh.py (camel/management)
    1. create doctree: parse main.py
    2. traverse doctree: populate database
'''

import os, re, time, shutil, logging, subprocess

from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from core.booktree import TexParser
from core.models import Module, BookNode

SITE_ROOT = getattr(settings, 'SITE_ROOT')
TEX_ROOT  = getattr(settings, 'TEX_ROOT')

out = logging.getLogger(__name__)

class Command(BaseCommand):
    '''
    Currently deletes the existing booktree entirely, which will be a problemm when answers
    and submissions point to question and assessment objects.
    '''
    args = 'module_code (, module_code, ...)'
    help = 'Update database for specified module codes'

    option_list = BaseCommand.option_list + (
        make_option("--text", action="store_true", dest="text", default=False, help="print document tree to stdout"),
        make_option("--xml", action="store_true", dest="xml", default=False, help="print xml tree to stdout"),
        make_option("--labels", action="store_true", dest="labels", help="print (label, mpath) pairs to stdout"),
        make_option("--db", action="store_true", dest="db", default=False, help="test write to database"),
        make_option("--commit", action="store_true", dest="commit", default=False, help="write to database"),
    )

    def handle(self, *args, **options):

        # process argument (module code)
        if not args:
            print 'Usage: python manage.py refresh <module_code> --option'
            return

        # info
        timestr = time.strftime("%Y.%m.%d.%H.%M.%S")
        out.info('Logging started at %s', timestr)
        # out.info('SITE_ROOT = %s' % SITE_ROOT)
        # out.info('TEX_ROOT  = %s' % TEX_ROOT)

        # iterate over modules
        for module_code in args:
            out.info('BEGIN processing %s', module_code)

            # find main.tex
            main_tex = os.path.join(TEX_ROOT, module_code, 'main.tex')

            # create book tree
            p = TexParser()
            preamble = p.parse_preamble( main_tex )
            book = p.parse_book( main_tex )
            book.title = preamble['book_title']

            # xml output
            if options['xml']:
                xml = book.prettyprint_xml()
                self.stdout.write( xml )

            # labels
            elif options['labels']:
                pairs = book.get_label_mpaths()
                col_width = max( [len(pair[0]) for pair in pairs] ) + 2  # padding
                for pair in pairs:
                    self.stdout.write( pair[0].ljust(col_width) + pair[1] )

            # database
            elif options['db'] or options['commit']:

                # check whether this module already exists in the database
                code = preamble['module_code']
                year = preamble['academic_year']
                modules = Module.objects.filter(code=code, year=year)
                if not modules:
                    out.info( 'Creating new module %s/%s' % (code, year) )
                    mo = Module(code=code, year=year, title=preamble['module_title'])
                    mo.save()
                elif len(modules) == 1:
                    out.info( 'Updating existing module %s/%s (existing doctree will be deleted)' % (code, year) )
                    mo = modules[0]
                    for bo in BookNode.objects.filter(module=mo):
                        bo.delete()
                else:
                    out.error('Error: database contains more than one (%s, %s)!' % (code, year) )
                    continue

                # hack to set user-defined latex macros
                nc = ''
                nc += r'\newcommand{\N}{\mathbb{N}}'
                nc += r'\newcommand{\Z}{\mathbb{Z}}'
                nc += r'\newcommand{\R}{\mathbb{R}}'
                nc += r'\newcommand{\C}{\mathbb{C}}'
                nc += r'\newcommand{\prob}{\mathbb{P}}'
                nc += r'\newcommand{\expe}{\mathbb{E}}'
                nc += r'\newcommand{\var}{\text{Var}}'
                nc += r'\newcommand{\cov}{\text{Cov}}'
                nc += r'\newcommand{\supp}{\text{supp}}'
                mo.newcommands = nc

                # save module
                mo.save()

                # write to database
                if options['commit']:
                    book.write_to_camel_database(module=mo, commit=True)
                else:
                    book.write_to_camel_database(module=mo, commit=False)

            # default: text output
            else:
                print book

        # end iterate over modules


