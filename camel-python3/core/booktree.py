#!/usr/bin/python
'''
doctree.py: build book tree from latex file (camel.cls)

    1. latex file -> book_tree
    2. book_tree -> xml
    3. book_tree <-> django models -> database objects

    #--------------------
    General
    #--------------------
    Block: non-leaf nodes (only name, title, label)
        Level, Theorem, List, Item, Homework, Figure, Table

    Content: leaf nodes
        Jax, Image, Label, Reference, Citation, Tabular
        
    *** Tabular should properly be a matrix of content nodes, some of which may be blocks
    *** This is tricky. For now, including environments in tabulars DOES NOT WORK.
    
    #--------------------
    Labels using materialized paths
    #--------------------
    Node.mpath is a string in the form 
    
    .001                book 1
    .001.001                chapter 1
    .001.002                chapter 2
    .001.002.001                section 1
    .001.002.002                section 2
    .001.002.003                section 3
    .001.003                 chapter 3
    
    Labels stored in a dictionary {text_label: 001.002.007.002.003}
    References implemented as {% url 'reference' label %} or similar

    #--------------------
    Labels
    #--------------------
    Labels refer to database objects, via the module_code.book_number.mpath identifier
    Only block nodes (non-leaf) can have labels, content nodes (leaf) cannot

    When we encounter a \label command, its contents (label_str) is listed alongside the current mpath
    This is embedded using <a href="#{{ node.label }}"> link

    When the associated \ref command is encountered, we insert a Reference object into the booktree
    This is rendered using <a href="{% url 'chapter-view' ref.get_parent_chapter %}#{{ ref.label }}"> 

      label:  <a name="anchor"></a>
      ref:    <a href="http://example..com/path/to/filename.html#anchor">Link Text</a>

    blocks:
      \label{ch:settheory}    <a name=#"MA1500.00.ch:settheory"></a> 
      \ref{ch:settheory}      <a href="MA1500.00.ch:settheory">the_chapter_number</a> 
      
    mathmode labels should be left to MathJax (tricky)  
      \label{eq:euler} to <a name="eq:euler"></a> 
      \ref{eq:euler}   to <a href="#eq:euler">the_equation_number</a> 

    The view extracts the linked object's numeric label (set automatically by parse_book )
    The root node Book() contains the label dictionary { "MA1500.00.eq:setthoery": "MA1500.00.01" } etc.

    output
      latex:  \begin{homework}\label{hw:week1} ... \end{homework}
      xml:    <homework label="hw:week1"> ... </homework>
      xhtml:  <div class="homework" label="hw:week1"> .. </div>
      object: Homework(type="homework", label="hw:week1")


    #--------------------
    database fields for basic book node
    #--------------------
    parent      parent
    node_id     serial number (not used by camel)

    #--------------------
    non-MathJax commands
    #--------------------
    
    level: (chapter|section|subsection)
    translate to <h1 class="chapter"> ... </h1>

    item: (item|question|part|subpart|choice|correctchoice)
    translate to <li class="question"> ... </li>
    
    source: (image|rev|cite)

    #--------------------
    css 
    #--------------------

    level: (chapter|section|subsection)
    translate to <h1 class="chapter"> ... </h1>

    item: (item|question|part|subpart|choice|correctchoice)
    translate to <li class="question"> ... </li>

    list: (itemize|enumerate|questions|parts|subparts)
    translate to <ul class="itemize"> ... </ul> etc.

    float: (table|subtable|figure|subfigure)
    translate to <img src="filename" number="1.3" caption="Onions" label="fig:onions" /> 
    translate to <div class="table" number="1.5" caption="Results" label="tab:results"> ... </div> 

    tabular: (tabular)
    translate to <table> ... </table>    

    assignment: (homework|singlechoice|multiplechoice)
    translate to <div class="homeworkc" number="2.2" label="hw:setheory"> ... </div>

    theorem: (definition|proposition|lemma|theorem|corollary)
    translate to <div class="lemma" number="3.1" caption="Zorn's Lemma" label="lem:zorn"> ... </div>

    box: (proof|solution|hint|hidebox|verbatim)
    translate to <div class="proof"> ... </div>

    content: (mathjax|image|ref|cite)


    To avoid writing nodes to the tree one-at-a-time
    context manager for mptt tree
        all context managers have __enter and __exit methods
        mptt has delay_mptt_update
            -> put this into the __enter

    involved with the "with" keyword (closes all within the context/scope )
    with file as f:
        etc
            

'''


#------------------------------------------------
# imports
import sys, os, re, logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

import core.models
from django.db.models import ImageField

#------------------------------------------------
# logging
out = logging.getLogger(__name__)

#------------------------------------------------
# classes
#------------------------------------------------

class Node(object):
    counter = 0    
    def __init__(self, parent=None):
        Node.counter += 1
        self.node_id = Node.counter
        self.children = []
        self.parent = parent
        
    # get mpath
    def mpath(self):
        if not self.parent:
            return ''
        idx = self.parent.children.index(self)
        hexstr = hex( idx )[2:].zfill(2)
        return self.parent.mpath() + '.' + hexstr

    
    # def hexlabel(self, index):
    #     return hex( idx )[2:].zfill(2)
        
    # "native" output
    def __repr__(self):
        s = ("%s" % self.mpath())
        s += ': '
        s += self.__class__.__name__ 
        if hasattr(self, 'number') and self.number:
            s += ': ' + str( self.number )
        if hasattr(self, 'title') and self.title:
            s += ': ' + self.title
        if hasattr(self, 'source') and self.content:
            s += ': ' + self.source
        if hasattr(self, 'htex') and self.htex:
            s += ': ' + self.htex
        s += '\n'
        for child in self.children:
            s += child.__repr__()
        return s
    
    
    # xml output
    def xml(self):
        element = ET.Element(self.__class__.__name__.lower())
        
        # set attributes
        # element.set('node_id', str(self.node_id))
        if hasattr(self, 'number') and self.number:
            element.set('number',  str(self.number))
        if hasattr(self, 'title') and self.title:
            element.set('title', self.title)
        if hasattr(self, 'label') and self.label:
            element.set('label', self.label)

        # set content 
        if hasattr(self, 'content') and self.content:
            element.text = self.content.strip()
       
        # recursive call
        for child in self.children:
            child_element = child.xml()
            element.append(child_element)
        return element

    # list of (label, mpath) pairs
    def get_label_mpaths(self):
        pairs = []
        if hasattr(self, 'label') and self.label:
            pairs.append( (self.label, self.mpath() ) )
        for child in self.children:
            pairs.extend( child.get_label_mpaths() )
        return pairs
    

    # camel output (writes to database)
    def write_to_camel_database(self, parent=None, commit=False, prefix=None, is_readonly=False):

        # create booknode
        booknode = core.models.BookNode(node_id=self.node_id)

        booknode.mpath = self.mpath()
        if prefix:
            booknode.mpath = prefix + booknode.mpath

        # set parent (if commit)
        if parent and commit:
            booknode.parent = parent

        # set attributes
        booknode.is_readonly = is_readonly            
        booknode.node_type = self.__class__.__name__.lower()
        booknode.node_class = node_class[booknode.node_type]
        if hasattr(self, 'label'):
            booknode.label = self.label
        if hasattr(self, 'number'):
            booknode.number = self.number
        if hasattr(self, 'title'):
            booknode.title = self.title
            
        if hasattr(self, 'content'):
            if booknode.node_type == "image":
                booknode.image = self.content
            else:
                booknode.text = self.content
                  
        # write to database
        print (booknode)
        if commit: 
            booknode.save()

        # recursive call
        for child in self.children:
            child.write_to_camel_database(parent=booknode, prefix=prefix, commit=commit)
            
        return booknode
        
#-----------------------------
# blocks: nodes with a title and/or label (both can be null)
#-----------------------------
class Block(Node):
    def __init__(self, title=None, label=None, parent=None):
        Node.__init__(self, parent=parent)
        self.title = title
        self.label = label

#-----------------------------
# book block (root)
#-----------------------------
class Book(Block):
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Chapter.number = 0
        Section.counter = 0
        Subsection.counter = 0
        Theorem.counter = 0
        Figure.counter = 0
        Table.counter = 0
        List.counter = 0

    # prettyprint xml tree
    def prettyprint_xml(self):
        xml_tree = self.xml()
        xml_str = ET.tostring(xml_tree, 'utf-8')
        dom = minidom.parseString(xml_str)
        proc_ins = dom.createProcessingInstruction('xml-stylesheet', 'type="text/css" href="xmlbook.css"')
        root = dom.firstChild
        dom.insertBefore(proc_ins, root)
        return dom.toprettyxml(indent="  ")

#-----------------------------
# level blocks
#-----------------------------
class Chapter(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Chapter.counter += 1
        self.number = Chapter.counter
        Section.counter = 0
        Subsection.counter = 0
        Theorem.counter = 0
        Homework.counter = 0
        Questions.counter = 0
        Figure.counter = 0
        Subfigure.counter = 0
        Table.counter = 0
        List.counter = 0
    
class Section(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Section.counter += 1
        self.number = Section.counter
        Subsection.counter = 0

class Subsection(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Subsection.counter += 1
        self.number = Subsection.counter
    
#-----------------------------
# theorem blocks
#-----------------------------
class Theorem(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Theorem.counter += 1
        self.number = Theorem.counter

class Lemma(Theorem):
    def __init__(self, title=None, label=None, parent=None):
        Theorem.__init__(self, title=title, label=label, parent=parent)

class Corollary(Theorem):
    def __init__(self, title=None, label=None, parent=None):
        Theorem.__init__(self, title=title, label=label, parent=parent)

class Definition(Theorem):
    def __init__(self, title=None, label=None, parent=None):
        Theorem.__init__(self, title=title, label=label, parent=parent)

class Remark(Theorem):
    def __init__(self, title=None, label=None, parent=None):
        Theorem.__init__(self, title=title, label=label, parent=parent)

class Example(Theorem):
    def __init__(self, title=None, label=None, parent=None):
        Theorem.__init__(self, title=title, label=label, parent=parent)

class Exercise(Theorem):
    def __init__(self, title=None, label=None, parent=None):
        Theorem.__init__(self, title=title, label=label, parent=parent)

#-----------------------------
# assignment blocks
#-----------------------------
class Assignment(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)

class Homework(Assignment):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Assignment.__init__(self, title=title, label=label, parent=parent)
        Homework.counter += 1
        self.number = Homework.counter

class Test(Assignment):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Assignment.__init__(self, title=title, label=label, parent=parent)
        Test.counter += 1
        self.number = Test.counter

class Singlechoice(Test):
    def __init__(self, title=None, label=None, parent=None):
        Test.__init__(self, title=title, label=label, parent=parent)

class Multiplechoice(Test):
    def __init__(self, title=None, label=None, parent=None):
        Test.__init__(self, title=title, label=label, parent=parent)

#-----------------------------
# list blocks (no title)
#-----------------------------
class List(Block):
    counter = 0
    def __init__(self, label=None, parent=None):
        Block.__init__(self, label=label, parent=parent)
        List.counter += 1
        self.number = List.counter
        Item.counter = 0

class Itemize(List):
    def __init__(self, label=None, parent=None):
        List.__init__(self, label=label, parent=parent)

class Enumerate(List):
    def __init__(self, label=None, parent=None):
        List.__init__(self, label=label, parent=parent)

class Questions(List):
    def __init__(self, label=None, parent=None):
        List.__init__(self, label=label, parent=parent)
        Question.counter = 0
        Part.counter = 0
        Subpart.counter = 0
        Choice.counter = 0

class Parts(List):
    def __init__(self, label=None, parent=None):
        List.__init__(self, label=label, parent=parent)
        Part.counter = 0
        Subpart.counter = 0
        Choice.counter = 0

class Subparts(List):
    def __init__(self, label=None, parent=None):
        List.__init__(self, label=label, parent=parent)
        Subpart.counter = 0
        Choice.counter = 0

class Choices(List):
    def __init__(self, label=None, parent=None):
        List.__init__(self, label=label, parent=parent)
        Choice.counter = 0

class Checkboxes(List):
    def __init__(self, label=None, parent=None):
        List.__init__(self, label=label, parent=parent)
        Choice.counter = 0

#-----------------------------
# item blocks (no title)
#-----------------------------
class Item(Block):
    counter = 0
    def __init__(self, label=None, parent=None):
        Block.__init__(self, label=label, parent=parent)
        Item.counter += 1
        self.number = Item.counter

class Question(Item):
    counter = 0
    def __init__(self, label=None, parent=None):
        Item.__init__(self, label=label, parent=parent)
        Question.counter += 1
        self.number = Question.counter

class Part(Item):
    counter = 0
    def __init__(self, label=None, parent=None):
        Item.__init__(self, label=label, parent=parent)
        Part.counter += 1
        self.number = Part.counter

class Subpart(Item):
    counter = 0
    def __init__(self, label=None, parent=None):
        Item.__init__(self, label=label, parent=parent)
        Subpart.counter += 1
        self.number = Subpart.counter

class Choice(Item):
    counter = 0
    def __init__(self, label=None, parent=None):
        Item.__init__(self, label=label, parent=parent)
        Choice.counter += 1
        self.number = Choice.counter

class Correctchoice(Choice):
    def __init__(self, label=None, parent=None):
        Choice.__init__(self, label=label, parent=parent)

#-----------------------------
# basic blocks (no title, no number, no label)
#-----------------------------
class Proof(Block):
    def __init__(self, parent=None):
        Block.__init__(self, parent=parent)

class Answer(Block):
    def __init__(self, parent=None):
        Block.__init__(self, parent=parent)

class Solution(Block):
    def __init__(self, parent=None):
        Block.__init__(self, parent=parent)

class Hint(Block):
    def __init__(self, parent=None):
        Block.__init__(self, parent=parent)

class Hidebox(Block):
    def __init__(self, parent=None):
        Block.__init__(self, parent=parent)

class Verbatim(Block):
    def __init__(self, parent=None):
        Block.__init__(self, parent=parent)

class Center(Block):
    def __init__(self, parent=None):
        Node.__init__(self, parent=parent)

#-----------------------------
# float blocks
#-----------------------------
class Figure(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Figure.counter += 1
        self.number = Figure.counter
        Subfigure.counter = 0

class Subfigure(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Subfigure.counter += 1
        self.number = Subfigure.counter

class Table(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Table.counter += 1
        self.number = Table.counter

class Subtable(Block):
    counter = 0
    def __init__(self, title=None, label=None, parent=None):
        Block.__init__(self, title=title, label=label, parent=parent)
        Subtable.counter += 1
        self.number = Subtable.counter


#-----------------------------
# leaf nodes (content blocks)
#-----------------------------
# Jax content:          mixture of html and latex
# Reference content:    text label
# Citation content:     text label
# Image content:        name of source file
# Script content:       code
class Content(Block):
    def __init__(self, content=None, label=None, parent=None):
        Block.__init__(self, label=label, parent=parent)
        self.content = content

class Reference(Content):
    ''' content: latex label '''
    def __init__(self, content=None, label=None, parent=None):
        Content.__init__(self, content=content, label=label, parent=parent)
        
class Citation(Content):
    ''' content: bibtex label '''
    def __init__(self, content=None, parent=None):
        Content.__init__(self, content=content, parent=parent)

class Tabular(Content):
    def __init__(self, content=None, parent=None):
        Content.__init__(self, label=label, parent=parent)

class Image(Content):
    ''' content: name of file containing the image '''
    def __init__(self, content=None, label=None, parent=None):
        Content.__init__(self, content=content, parent=parent)

class Script(Content):
    ''' content: is python code for checking answers '''
    def __init__(self, content=None, label=None, parent=None):
        Content.__init__(self, content=content, label=label)
        
                
class Jax(Content):
    def __init__(self, content=None, label=None, parent=None):
        Content.__init__(self, content=content, label=label, parent=parent)
        
        # check for nothing-but-whitespace (if so, set content to empty string)
        # we test for empty content nodes (and delete them) later.
        # this should be done in the calling environment so that empty
        # content nodes are not included.
        # if not content or not re.compile(r'\S+',re.DOTALL).search(content):
        #     self.htex = ''
        #     return
        
        # remove comments (line-by-line) - now done in TexParser.read_latex_file()
        # lines = content.strip().split('\n')
        # for idx in range( len(lines) ):
        #     lines[idx] = re.sub(r'\%.*$', "", lines[idx])
        # s = '\n'.join(lines) + '\n'
        
        s = content
        
        # temporary hack: kill mathmode labels (MathJax can be configured to handle these)
        s = re.sub(r'\\label\{([^\}]*)\}', r'',s)

        # font styles
        s = re.sub(r'\\emph\{([^\}]*)\}',r'<i>\1</i>',s)
        s = re.sub(r'\\textit\{([^\}]*)\}',     r'<i>\1</i>',s)
        s = re.sub(r'\\textbf\{([^\}]*)\}',     r'<b>\1</b>',s)
        s = re.sub(r'\\texttt\{([^\}]*)\}',     r'<tt>\1</tt>',s)
        s = re.sub(r'\\underline\{([^\}]*)\}',  r'<u>\1</u>',s)
        
        # spacing
        s = re.sub(r'\\vspace[\*]?\{[^\}]\w+\}',r'<p>',s)
        s = re.sub(r'\\hspace[\*]?\{[^\}]\w+\}',r'&nbsp;&nbsp;',s)
        
        # custom
        s = re.sub(r'\\proofomitted',           r'<i>[Proof omitted]</i><br/>', s)

        # layout
        s = re.sub(r'\\paragraph\{([^\}]*)\}',  r'<br>\n<b>\\1</b>\n',s)
        s = re.sub(r'\\par\s+',                 r'<br>',s)
        s = re.sub(r'\\bigskip\s+',             r'<br>',s)

        # tricky
        s = re.sub(r'\\percent', r'&#37;',s)
        s = re.sub(r'\\\&', r'&amp;',s)
        s = re.sub(r'~', r'&nbsp;',s)
        
        # kill
        s = re.sub(r'\\maketitle',          r'',s)
        s = re.sub(r'\\tableofcontents',    r'',s)
        s = re.sub(r'\\makefrontmatter',    r'',s)
        s = re.sub(r'\\clearpage',          r'',s)
        s = re.sub(r'\\cleardoublepage',    r'',s)
        s = re.sub(r'\\break',              r'',s)
        s = re.sub(r'\\newpage',            r'',s)
        s = re.sub(r'\\label\{.*\}',        r'',s)  # already extracted
        s = re.sub(r'\\centering',          r'',s)
        s = re.sub(r'\\hfill',              r'',s)
        s = re.sub(r'\\vfill',              r'',s)
        s = re.sub(r'\\if.*',               r'',s)
        s = re.sub(r'\\small',              r'',s)
        s = re.sub(r'\\normalsize',         r'',s)
        s = re.sub(r'\\endinput',           r'',s)
        s = re.sub(r'\ ',                   r' ',s)
            
        # set field value (tidy up)
        self.content = s.strip()
    



# boilerplate code

#-----------------------------
# lookup tables
#-----------------------------
# assign node_types to node_classes
# used to find the set of node_types belonging to a given node_class 
node_types = {
    'assignment': ('homework', 'singlechoice', 'multiplechoice'),
    'box': ('proof', 'solution', 'answer', 'hint', 'verbatim', 'center'),
    'content': ('image', 'jax', 'reference', 'citation', 'tabular'),
    'level': ('book', 'chapter', 'section', 'subsection'),
    'float': ('table', 'figure', 'subfigure'),
    'mathmode': ('equation', 'eqnarray', 'array', 'align', 'cases'),
    'item': ('item', 'part', 'question', 'subpart', 'choice', 'correctchoice'),
    'list': ('itemize', 'enumerate',  'questions', 'parts', 'subparts', 'choices', 'checkboxes'),
    'theorem': ('definition', 'theorem', 'lemma',  'corollary',  'remark', 'example', 'exercise')
}

# lookp table to find out which node_class a given node_type belongs to
node_class = dict([ (k2,k1) for k1 in node_types.keys() for k2 in node_types[k1] ])

# item dictionary (which items should be used in which environments)
item_dict = {
    'itemize':      'item',
    'enumerate':    'item',
    'questions':    'question',
    'parts':        'part',
    'subparts':     'subpart',
    'choices':      'choice|correctchoice',
    'checkboxes':   'choice|correctchoice',
}

# dictionary of classes corresponding to node_type
# doctree_class = {
#     'level': {
#         'book':             Book,
#         'chapter':          Chapter,
#         'section':          Section,
#         'subsection':       Subsection,
#     },
#     'list':     {
#         'itemize':          Itemize,
#         'enumerate':        Enumerate,
#         'questions':        Questions,
#         'parts':            Parts,
#         'subparts':         Subparts,
#         'choices':          Choices,
#         'checkboxes':       Checkboxes,
#     },
#     'item':     {
#         'item':             Item,
#         'question':         Question,
#         'part':             Part,
#         'subpart':          Subpart,
#         'choice':           Choice,
#         'correctchoice':    Correctchoice,
#     },
#     'assignment': {
#         'homework':         Homework,
#         'singlechoice':     Singlechoice,
#         'multiplechoice':   Multiplechoice,
#     },
#     'float': {
#         'figure':           Figure,
#         'table':            Table,
#         'subfigure':        Subfigure,
#         'subtable':         Subtable,
#     },
#     'theorem':  {
#         'theorem':          Theorem,
#         'definition':       Definition,
#         'lemma':            Lemma,
#         'corollary':        Corollary,
#         'remark':           Remark,
#         'example':          Example,
#         'exercise':         Exercise,
#     },
#     'box': {
#         'proof':        Proof,
#         'answer':       Answer,
#         'solution':     Solution,
#         'hint':         Hint,
#         'verbatim':     Verbatim,
#         'center':       Center,
#     },
#     'mathmode': {
#         'equation':     None,
#         'eqnarray':     None,
#         'cases':        None,
#         'align':        None,
#         'array':        None,
#     },
#     'content': {
#         'jax':          Jax,
#         'tabular':      Tabular,
#         'image':        Image,
#         'reference':    Reference,
#         'citation':     Citation,
#     },
# }

# # node_type grouped by node_class
# node_types = { key : tuple( doctree_class[key].keys() ) for key in doctree_class.keys() }
    
# node_class grouped by node_type
# node_class = dict([ (k2,k1) for k1 in cldoctree_class.keys() for k2 in doctree_class[k1].keys() ])


# dictionary of classes corresponding to node_type
class_lookup = {
    'book':             Book,
    'chapter':          Chapter,
    'section':          Section,
    'subsection':       Subsection,
    'itemize':          Itemize,
    'enumerate':        Enumerate,
    'questions':        Questions,
    'parts':            Parts,
    'subparts':         Subparts,
    'choices':          Choices,
    'checkboxes':       Checkboxes,
    'item':             Item,
    'question':         Question,
    'part':             Part,
    'subpart':          Subpart,
    'choice':           Choice,
    'correctchoice':    Correctchoice,
    'homework':         Homework,
    'singlechoice':     Singlechoice,
    'multiplechoice':   Multiplechoice,
    'figure':           Figure,
    'table':            Table,
    'subfigure':        Subfigure,
    'subtable':         Subtable,
    'theorem':          Theorem,
    'definition':       Definition,
    'lemma':            Lemma,
    'corollary':        Corollary,
    'remark':           Remark,
    'example':          Example,
    'exercise':         Exercise,
    'proof':            Proof,
    'answer':           Answer,
    'solution':         Solution,
    'hint':             Hint,
    'verbatim':         Verbatim,
    'center':           Center,
    'jax':              Jax,
    'tabular':          Tabular,
    'image':            Image,
    'reference':        Reference,
    'citation':         Citation,
    'equation':         None,
    'eqnarray':         None,
    'cases':            None,
    'align':            None,
    'array':            None,
}

#-----------------------------
# TexParser class (root node of document tree)
class TexParser(object):
    # init
    def __init__(self):
        pass
    
    def read_latex_file(self, filename, level=0):
        if level > 4:
            print('error: read_body: recursion limit reached (max = 4)')
            return ''
        
        # open file
        with open(filename) as f:
            f_str = f.read()
        
            # remove comments (line-by-line)
            lines = f_str.strip().split('\n')
            for idx in range( len(lines) ):
                lines[idx] = re.sub(r'\%.*$', "", lines[idx])
            f_str = '\n'.join(lines) + '\n'
        
            # find input commands
            pattern = re.compile(r'[^%+]\\input\{([^\}]*)\}')
            matches = re.finditer(pattern, f_str)
            
            # return contents if no \input commands (end recursion)
            if not matches:
                return f_str
            
            # otherwise process \input commands
            else:
                s = ''
                start_index = 0
                for match in matches:
                    end_index = match.start()
                    s += f_str[ start_index:end_index ]
                    start_index = match.end()
                    nested_filename = match.groups()[0]
                    # append .tex extension if necessary
                    if not re.search(r'\.', nested_filename):
                        nested_filename = nested_filename + '.tex'
                    nested_filename = os.path.join(os.path.dirname(filename), nested_filename)
                    out.info('File: %s', nested_filename)
                    # recursive call
                    s += self.read_latex_file(nested_filename, level=level+1)
                s += f_str[start_index:]
                return s
    
    
    def read_preamble(self, filename):
        with open(filename) as f:
            f_str = f.read()
            pattern = r'(.*)\\begin\{document\}' 
            match = re.compile(pattern, re.DOTALL).search( f_str )
            preamble = match.groups()[0] if match else ''
            return preamble

    def check_preamble(self, main_file="main.tex"):
        '''
        check document class and mandatory commands
        '''
        preamble = self.read_preamble( main_file )
    
        # document class (should be "camel" with no options) 
        pattern = r'\\documentclass(\[.*\])?\{([^\}]+)\}'
        match = re.compile(pattern).search( preamble )
        if not match or not match.groups()[1] == 'camel':
            out.error('document class must be "camel"')
            print('document class must be "camel"')
            return False

        # module code
        match = re.compile(r'\\modulecode\{(\w+)\}').search( preamble )
        if not match:
            out.error(r'\modulecode{} missing in preamble')
            print(r'\modulecode{} missing in preamble')
            return False

        # academic year
        match = re.compile(r'\\academicyear\{(.*)\}').search( preamble )
        if not match:
            out.error(r'\academicyear{} missing in preamble')
            print(r'\academicyear{} missing in preamble')
            return False
            
        # ok
        return True
    
    def read_body(self, filename):
        s = self.read_latex_file(filename)
        s = self.fix_latex(s)
        pattern = r'\\begin{document}(.*)\\end{document}' 
        match = re.compile(pattern, re.DOTALL).search( s )
        body = match.groups()[0] if match else ''
        return body

    def fix_latex(self, s):
        s = re.sub(r'\\bit\s+', r'\\begin{itemize} ', s)
        s = re.sub(r'\\eit\s+', r'\\end{itemize} ', s)
        s = re.sub(r'\\ben\s+', r'\\begin{enumerate} ', s)
        s = re.sub(r'\\een\s+', r'\\end{enumerate} ', s)
        s = re.sub(r'\\it\s+', r'\\item ', s)
        return s
        
    def make_book(self, main_file="main.tex"):

        # check preamble
        if not self.check_preamble( main_file ):
            out.error('Errors in main.tex - aborting.')
            print('Errors in main.tex - aborting.')
            return None

        preamble = self.parse_preamble( main_file )
        tree = self.parse_body( main_file )
        
        book = Book()
        book.tree = tree
        if 'book_title' in preamble:
            book.title = preamble['book_title']
        if 'book_author' in preamble:
            book.author = preamble['book_author']
        if 'book_version' in preamble:
            book.version = preamble['book_version']
        if 'new_commands' in preamble:
            book.new_commands = preamble['new_commands']
        return book

    def parse_book(self, main_file="main.tex"):

        # check preamble
        if not self.check_preamble( main_file ):
            out.error('Errors in main.tex - aborting.')
            print('Errors in main.tex - aborting.')
            return None

        # preamble = self.parse_preamble( main_file )
        book = self.parse_body( main_file )
        # if 'book_title' in preamble:
        #     book.title = preamble['book_title']
        # if 'book_author' in preamble:
        #     book.author = preamble['book_author']
        # if 'book_version' in preamble:
        #     book.version = preamble['book_version']
        # if 'new_commands' in preamble:
        #     book.new_commands = preamble['new_commands']
        return book

    def parse_preamble(self, main_file):    

        preamble  = self.read_preamble( main_file )
        preamble_data = {
            # 'module_code':      None,
            # 'academic_year':    None,
            # 'module_title':     None,
            # 'book_number':      None,
            # 'book_title':       None,
            # 'new_commands':     '',
        }
        match = re.compile(r'\\modulecode\{(\w+)\}').search( preamble )
        if match: 
            preamble_data['module_code'] = match.groups()[0]

        match = re.compile(r'\\academicyear\{(.*)\}').search( preamble )
        if match: 
            preamble_data['academic_year'] = match.groups()[0]

        match = re.compile(r'\\moduletitle\{(.*)\}').search( preamble )
        if match: 
            preamble_data['module_title'] = match.groups()[0]

        match = re.compile(r'\\booknumber\{(.*)\}').search( preamble )
        if match:
            preamble_data['book_number'] = match.groups()[0]

        match = re.compile(r'\\booktitle\{(.*)\}').search( preamble )
        if match:
            preamble_data['book_title'] = match.groups()[0]

        match = re.compile(r'\\bookauthor\{(.*)\}').search( preamble )
        if match:
            preamble_data['book_author'] = match.groups()[0]

        match = re.compile(r'\\bookversion\{(.*)\}').search( preamble )
        if match:
            preamble_data['book_version'] = match.groups()[0]

        # newcommands (keep as latex for mathjax to handle)
        newcmds = []    
        pattern = re.compile(r'(\\newcommand\{[^\}]*\}\{.*\})') # dodgy
        matches = re.finditer(pattern, preamble)
        for match in matches:
            newcmds.append( match.groups()[0] )
        # defs
        pattern = re.compile(r'(\\def\\(\w+)\{.*\})') # dodgy
        matches = re.finditer(pattern, preamble)
        for match in matches:
            newcmds.append( match.groups()[0] )

        preamble_data['new_commands'] = '\n'.join( newcmds )
        return preamble_data


    def parse_body(self, main_file):
        '''
        1. Chop into chapters/sections/subsections.
            LaTeX allows content *before* the first chapter etc., so this is tricky. 
            We want to avoid creating a "Chapter 0", "Section 0.1" and so on.
            The children of the Book element should just be a sequence of BookNodes
            This method uses recursion (with an explicit stack), but it pays off later.
            The resulting structure is as follows:
            book:
                - block
                - chapter
                    - block
                    - section
                        -block
                        -subsection
                            -block
                        -subsection
                            -block
                    - section
                        -block
                - chapter
                    - block
                - chapter
                    - block
                    - section
                        -block
            
        2. Call parse_snippet recursively on the resulting blocks
            We have recursed down through chapters, sections and subsections
            We now proceed to process the blocks that these represent
        '''
        
        # extract body
        body = self.read_body( main_file )

        # find all level commands 
        pattern = r'\\(chapter|section|subsection)\{([^\}]*)\}'
        matches = re.finditer(pattern, body)

        # init stack
        root = Book()
        stack = [ root ]
        start_idx = 0
        
        # iterate over level commands
        for match in matches: 
            node_type   = match.groups()[0]     # chapter, section or subsection
            node_title  = match.groups()[1]    # title
            end_idx   = match.start()            # end index of block before current level command
            tex_str     = body[ start_idx : end_idx ]

            # Call parse_snippet on tex_str
            # This tex_str is the block located BEFORE the current level command
            # The tex_str located after the very last level command is processed separately at the end
            children = self.parse_snippet( tex_str, parent=stack[-1] )
            # for child in children:
            #     child.parent = stack[-1]
            stack[-1].children.extend( children )
            # stack[-1].label = label

            # chapter/section/subsection: close current subsection (if any) and append it to enclosing section
            if node_type in ['chapter', 'section', 'subsection']:
                if type(stack[-1]) == Subsection:
                    ss = stack.pop()
                    stack[-1].children.append( ss )
                # chapter/section: close current section (if any) and append it to enclosing chapter
                if node_type in ['section', 'chapter']:
                    if type(stack[-1]) == Section:
                        se = stack.pop()
                        stack[-1].children.append( se )
                    # chapter: close current chapter (if any) and append it to document root
                    if node_type == 'chapter':
                        if type(stack[-1]) == Chapter:
                            ch = stack.pop()
                            stack[-1].children.append( ch )
                        # push new chapter onto stack
                        ch = Chapter( node_title )
                        ch.parent = stack[-1]
                        stack.append( ch )
                    # push new section onto stack
                    else:
                        se = Section( node_title )
                        se.parent = stack[-1]
                        stack.append( se )
                # push new subsection onto stack
                else: 
                    ss = Subsection( node_title )
                    ss.parent = stack[-1]
                    stack.append( ss )

            # update start_idx for next match
            start_idx = match.end()

        # clean up tail (after last match has been processed)
        # last level command could be chapter, section or subsection
        tex_str = body[ start_idx : len(body) ]
        children = self.parse_snippet( tex_str, parent=stack[-1] )
        # for child in children:
        #     child.parent = stack[-1]
        last_level = stack.pop()
        last_level.children.extend( children )
        # last_level.label = label
        stack[-1].children.append( last_level )    # append last level to parent

        # pop off enclosing environments until we reach the root
        while len(stack) > 1:
            node = stack.pop()
            stack[-1].children.append( node )

        # return the root node (book)
        return stack.pop()   
    
    def chop_snippet(self, snippet):
        '''
        returns list of [node_type, node_title, start_idx, end_idx] 
            0: node_type    'tex' or environment name
            1: node_title (only for environments)
            2: start_idx    overkill: one array of cut_points would be enough
            3: end_idx
            
        List alternates as [tex, env, tex, env, ... , env, tex]
            Starts and ends with tex nodes
            
        1. tex_str chopped up on \begin{environment} and \end{environment}
        2. list process using a stack (to pair every \begin with its \end)

        Only level-one environments are extracted. Any environments nested within level-one
        environments are processed recursively by parse_snippet
        
        '''
        # initialise 
        stack = []
        blocks = []     # ['tex' or environment_name, title (if any), sub-snippet]
        
        # append first block: always a content block (empty blocks are removed later)
        # Initially it contains the entire tex string
        # The end_index will be overwritten unless "tex_str" contains only one block
        # The final entry is the block title
        blocks.append([ 'tex', '', 0, len(snippet) ])

        # find all environment delimiters 
        # catches environment names (optional argument)
        # careful: also catches tabular column format string (second curly-braces)
        pattern = r'\\(begin|end)\{(\w+)\}(\[(.*)\]|\{(.*)\})*'
        matches = re.finditer(pattern, snippet)

        # old school
        timeout=False
        timeout_name = None
        
        # loop over environment delimiters
        for match in matches: 
            
            # process current match
            groups = match.groups()
            
            # descriptive names
            begin_or_end           = groups[0]
            environment_name       = groups[1]
            environment_title      = groups[3] if groups[3] else None
            
            # at "begin"
            if begin_or_end == 'begin':
                # start timeout if beginning of mathmode environment
                if environment_name in node_types['mathmode']:
                    timeout = True
                    timeout_name = environment_name
                # process if not inside mathmode environment
                if not timeout:
                    # push environment name onto stack
                    stack.append( environment_name )
                    # extend slices only if at beginning of level-one environment
                    if len(stack) == 1:
                        # set end_idx of preceeding block
                        blocks[-1][3] = match.start()
                        # append new sub-snippet for current environment (contains the rest of the snippet)
                        blocks.append([ environment_name, environment_title, match.end(), len(snippet) ])
            # at "end"
            else:
                if not timeout:
                    # pop name off stack (and check that it co-incides with current node_type )
                    assert environment_name == stack.pop()
                    # add block only if end of level-one environment
                    if len(stack) == 0:
                        # set end_idx of previous block
                        blocks[-1][3] = match.start()
                        # append new tex block (to cap off this environment)
                        blocks.append([ 'tex', '', match.end(), len(snippet) ])
                # stop timeout if end of corresponding mathmode environment
                else:
                    # end timeout if necessary
                    if environment_name == timeout_name:
                        timeout = False
        return blocks

    
    
    def parse_snippet(self, snippet, parent=None):
        '''
        First calls chop_snippet, which returns a list of substrings
        List alternates as [tex, env, tex, env, ... , env, tex]
            i.e. starts and ends with tex nodes
            The 
            
        This only processes level-one environments. Any environments nested within level-one
        environments are processed recursively
        
        rationale: "parent" is passed because tex_str is stripped of its "context"
        however this is already implicit, because the parent will contain a list of
        child nodes in the correct order: the parent link is needed to make computing
        mpaths easy.
        '''
        
        #----------------------------------------
        # find sub-snippets, their types and their titles
        # (crazy) format is [node_types_name, node_title, start_idx, end_idx]
        blocks = self.chop_snippet( snippet )
        # snippet, snippet_type, snippet_title = self.chop_snippet(tex_str)

        # initialise list of children (return value)
        children = []

        # iterate through sub-snippets
        for block in blocks:

            # use descriptive names (recycle name 'snippet' )
            snip_type = block[0]
            snip_title = block[1]
            snip = snippet[ block[2]: block[3] ]

            # tex snippet (contain no non-mathmode environments)
            #   jax: mixture of html and latex commands
            #   tabular: hack into a jax string
            #   drawback:  can't use tabular to set out figures
            if snip_type == 'tabular':
                
                # check for nothing-but-whitespace
                if not snip or not re.compile(r'\S+',re.DOTALL).search(snip):
                    continue

                # kill horizontal lines
                snip = re.sub(r'\\hline','', snip)

                htex = '<table class="tabular">'
                # split table rows on double fowrard slash
                rows = snip.split(r'\\')
                for row in rows:
                    if not row or not re.compile(r'\S+',re.DOTALL).search(row):
                        break
                    htex += '<tr>'
                    # split table elements on ampersand
                    cells = row.split(r'&')
                    for cell in cells:
                        htex += '<td>' + cell + '</td>'
                    htex += '</tr>'
                htex += '</table>'
                
                children.append( Jax( content=htex, parent=parent ) )
                                
            # tex snip (inline stuff done here)
            elif snip_type == 'tex':
                
                # check for nothing-but-whitespace
                if not snip or not re.compile(r'\S+',re.DOTALL).search(snip):
                    continue

                # find and extract label text, then attach to parent
                label = None
                pattern = r'\\label\{([^\}]*)\}'
                match = re.search(pattern, snip)
                if match and parent:
                    parent.label = match.groups()[0]
        
                # images (parse contents of figure or subfigure environment)
                # match = re.compile(r'\\includegraphics(\[[^\]]*\])\{([^\}]+)\}').search(snip)
                match = re.compile(r'\\includegraphics(\[[^\]]*\])*\{([^\}]+)\}').search(snip)
                if match:
                    src = match.groups()[1] 
                    children.append( Image( content=src, parent=parent ) )

                else:
                    pattern = r'\\(ref|cite)\{([^\}]+)\}'
                    matches = re.finditer(pattern, snip)
                    if not matches:
                        if not snip or not re.compile(r'\S+',re.DOTALL).search(snip):
                            continue
                        children.append( Jax( content=snip, label=label, parent=parent ) )
                    else:
                        start_idx = 0;
                        for match in matches: 
                            end_idx = match.start()
                            ref_text = match.groups()[0]
                            jax_snip = snip[ start_idx: end_idx ]
                            if not jax_snip or not re.compile(r'\S+',re.DOTALL).search(jax_snip):
                                continue
                            children.append( Jax( content=jax_snip, label=label, parent=parent ) )
                            if match.groups()[1] == 'ref':
                                children.append( Reference( content=ref_text, parent=parent ) )
                            elif match.groups()[1] == 'cite':
                                children.append( Citation( content=ref_text, parent=parent ) )
                            start_idx = match.end()
                        # process final jax snippet
                        jax_snip = snip[ start_idx: ]
                        if not jax_snip or not re.compile(r'\S+',re.DOTALL).search(jax_snip):
                            continue
                        children.append( Jax( content=jax_snip, label=label, parent=parent ) )
            
            # containers
            else:
                classname = class_lookup[ snip_type ]
                node = classname( parent=parent )
                
                # node = eval( snip_type.capitalize() )( parent=parent )
                # print '=========================================='
                # print snip_type
                # print type(node)
                # print '=========================================='

                # mathmode: equation, eqnarray, align, array (no children)
                if snip_type in node_types['mathmode']:
                    return []
            
                # lists
                elif snip_type in node_types['list']:
                    item_name = item_dict[snip_type] # item, question, part, subpart, choice
                    node.children = self.parse_list_contents(snip, parent=node, item_name=item_name)            
            
                # float: tables, figures, subfigures (extract caption and set as title)
                elif snip_type in node_types['float']:
                    match = re.compile(r'\\caption\{([^\}]+)\}').search(snip)
                    if match:
                        node.title = match.groups()[0]
                        snip = snip[:match.start()] + snip[match.end():]
                    node.children = self.parse_snippet( snippet=snip, parent=node )

                # all others
                else:
                    if snip_title: 
                        node.title = snip_title
                    node.children = self.parse_snippet( snippet=snip, parent=node )

                children.append(node)
            
        return children

    
    def parse_list_contents(self, snippet, parent=None, item_name="item"):
        '''
        Returns list of item nodes (becomes the children of the enclosing list node)
        '''

       # check item name is valid
        # if item_name not in node_types['item']:
        #     return None

        # function to extract next item snippet
        def find_next_item(snippet, item_name='item'):
            '''
            string processing function that skips over environments to find the next item snippet
            '''
            
            # find all item tokens and environment delimiters
            pattern = r'\\(' + item_name + r')|\\(begin|end)\{(\w+)\}' 
            matches = re.finditer(pattern, snippet)
            
            # return the entire snippet if no matches at all
            if not matches:
                return snippet, ''

            # get first match and make sure it's an item (not an environment delimiter)
            first_match = matches.next()
            if not first_match.groups()[0]:
                return snippet, []
            
            # set item type (needed to distinguish between \choice and \correctchoice)
            item_type = first_match.groups()[0]
            
            # use stack to keep track of levels
            start_idx = first_match.end()
            stack = []
            for match in matches:
                groups = match.groups()
                if groups[1]:
                    if groups[1] == 'begin':
                        stack.append( groups[2] )
                    else:
                        stack.pop()
                else:
                    # return to calling environment when stack empty (next item reached)
                    if len(stack) == 0:
                        end_idx = match.start()
                        return snippet[start_idx:end_idx], snippet[ end_idx: ], item_type

            # return final item snippet
            return snippet[ start_idx: ], '', item_type

        # init list to hold items
        item_list = []
        
        # chop up list (recursive call to parse_snippet here)
        tail = snippet
        while tail:
            snip, tail, item_type = find_next_item(tail, item_name=item_name)
            classname = class_lookup[ item_type ]
            item = classname( parent=parent )
            # item = eval( item_type.capitalize() )(parent=parent)
            item.children = self.parse_snippet( snippet=snip, parent=item  )
            item_list.append( item )

        return item_list





#------------------------------------------------
# main
# command line options are mirrored in camel/management/commands
#------------------------------------------------
def main(args=None):
    
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [-v] [-q] [-x] [latex_main]", version="%prog: version 0.1", add_help_option=True)
    parser.add_option("-v", "--verbose", action="store_false", dest="verbose", help="verbose output")
    parser.add_option("-t", "--text", action="store_true", dest="text", help="print text tree to stdout")
    parser.add_option("-x", "--xml", action="store_true", dest="xml", help="print xml tree to stdout")
    parser.add_option("-l", "--labels", action="store_true", dest="labels", help="print (label, mpath) pairs to stdout")
    parser.add_option("-d", "--db", action="store_true", dest="db", help="update camel database (dry run)")
    parser.add_option("-c", "--commit", action="store_true", dest="commit", help="update camel database (commit changes)")
    parser.set_defaults(verbose=True, demo=False, text=False, xml=False, camel=False, commit=False)

    (options, args) = parser.parse_args()
    if not args:
        print ('usage: $python doctree.py main.tex (camel.cls)')
        return

    # parse
    main_tex = args[0]
    p = TexParser()
    book = p.parse_book( main_tex )

    # text output (native format)
    if options.text:
        print (book)

    # xml output
    if options.xml:
        xml_file = open("xmlbook.xml","w")
        xml_file.write("%s" % book.prettyprint_xml() )
        xml_file.close()        
        print (book.prettyprint_xml())

    # labels
    if options.labels:
        pairs = book.get_label_mpaths()
        col_width = max( [len(pair[0]) for pair in pairs] ) + 2  # padding
        for pair in pairs:
            print (pair[0].ljust(col_width) + pair[1])

    # camel database output
    if options.db:
        
        # check whether this module already exists in the database
        preamble = p.parse_preamble( main_tex )
        code = preamble['module_code']
        year = preamble['academic_year']
        module = core.models.Module.objects.filter(code=code, year=year).first()
        if not module:
            out.info( 'Creating new module %s/%s' % (code, year) )
            module = core.models.Module(code=code, year=year, title=preamble['module_title'])
            module.save()
        else:
            out.info( 'Updating existing module %s/%s' % (code, year) )
        number = preamble['book_number']
        bk = module.book_set.filter(number=number).first()
        if bk:
            out.info( 'Existing book %s/%s/%s will be deleted' % (code, year, number) )
            for booknode in core.models.BookNode.objects.filter(mpath__startswith=bk.tree.mpath):
                booknode.delete()
            bk.delete()
        

        camel_book = core.models.Book()
        code = preamble['module_code']
        year = preamble['academic_year']
        
        camel_book.module = core.models.Module.objects.filter(code=code, year=year).first()
        if 'book_number' in preamble:
            camel_book.number = int(preamble['book_number'])
        else:
            camel_book.number = 0
        if 'book_title' in preamble:
            camel_book.title = preamble['book_title']
        if 'book_author' in preamble:
            camel_book.author = preamble['book_author']
        if 'book_version' in preamble:
            camel_book.version = preamble['book_version']
        if 'new_commands' in preamble:
            camel_book.new_commands = preamble['new_commands']
            
        hexstr = hex( camel_book.number )[2:].zfill(2)
        prefix = code + '.' + hexstr

        # write book database
        if options.commit:
            camel_book.tree = book.write_to_camel_database(prefix=prefix, commit=True)
            camel_book.save()
            
        else:
            book.write_to_camel_database(prefix=prefix, commit=False)
          
        # write labels to database
        pairs = book.get_label_mpaths()
        for pair in pairs:
            lab = core.models.Label()
            lab.book = camel_book
            lab.text = prefix + '.' + pair[0]
            lab.mpath = prefix + pair[1]
            if options.commit:
                lab.book = cbook
                lab.save()
            else:
                print (lab)
          
if __name__ == '__main__':
    main()

