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
from core.models import Module, BookNode, Book, Label

SITE_ROOT = getattr(settings, 'SITE_ROOT')
TEX_ROOT  = getattr(settings, 'TEX_ROOT')

out = logging.getLogger(__name__)

class Command(BaseCommand):
    '''
    Currently deletes the existing book entirely, which will be a problemm when answers
    and submissions point to question and assessment objects.
    '''
    args = 'module_code (, module_code, ...)'
    help = 'Update database for specified module codes'

    option_list = BaseCommand.option_list + (
        make_option("--text", action="store_true", dest="text", default=False, help="print document tree to stdout"),
        make_option("--xml", action="store_true", dest="xml", default=False, help="print xml tree to stdout"),
        make_option("--labels", action="store_true", dest="labels", help="print (label, mpath) pairs to stdout"),
        make_option("--db", action="store_true", dest="db", default=False, help="write to database"),
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

            # parse
            p = TexParser()
            tree = p.parse_book( main_tex )

            # text output (native format)
            if options['text']:
                print tree

            # xml output
            if options['xml']:
                xml = tree.prettyprint_xml()
                self.stdout.write( xml )

            # labels
            if options['labels']:
                pairs = tree.get_label_mpaths()
                col_width = max( [len(pair[0]) for pair in pairs] ) + 2  # padding
                for pair in pairs:
                    self.stdout.write( pair[0].ljust(col_width) + pair[1] )

            # database
            if options['db'] or options['commit']:

                # check whether this module already exists in the database
                preamble = p.parse_preamble( main_tex )
                code = preamble['module_code']
                year = preamble['academic_year']
                module = Module.objects.filter(code=code, year=year).first()
                if not module:
                    out.info( 'Creating new module %s/%s' % (code, year) )
                    module = Module(code=code, year=year, title=preamble['module_title'])
                    module.save()
                else:
                    out.info( 'Updating existing module %s/%s' % (code, year) )
                number = preamble['book_number']
                book = Book.objects.filter(module=module, number=number).first()
                if book:
                    out.info( 'Existing book %s/%s/%s will be deleted' % (code, year, number) )
                    for booknode in BookNode.objects.filter(mpath__startswith=book.tree.mpath):
                        booknode.delete()
                    book.delete()
        

                book = Book()
                code = preamble['module_code']
                year = preamble['academic_year']
        
                book.module = Module.objects.filter(code=code, year=year).first()
                if 'book_number' in preamble:
                    book.number = int(preamble['book_number'])
                else:
                    book.number = 0
                if 'book_title' in preamble:
                    book.title = preamble['book_title']
                if 'book_author' in preamble:
                    book.author = preamble['book_author']
                if 'book_version' in preamble:
                    book.version = preamble['book_version']
                if 'new_commands' in preamble:
                    book.new_commands = preamble['new_commands']
            
                hexstr = hex( book.number )[2:].zfill(2)
                prefix = code + '.' + hexstr

                # write book database
                if options['commit']:
                    book.tree = tree.write_to_camel_database(prefix=prefix, commit=True)
                    book.save()
            
                else:
                    tree.write_to_camel_database(prefix=prefix, commit=False)
          
                # write labels to database
                pairs = tree.get_label_mpaths()
                for pair in pairs:
                    lab = Label()
                    lab.book = book
                    lab.text = prefix + '.' + pair[0]
                    lab.mpath = prefix + pair[1]
                    if options['commit']:
                        lab.save()
                    else:
                        print lab



