# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

# these should be moved to settings.py
ACADEMIC_YEARS = (
    ('2014-15', '2014-15'),
    ('2015-16', '2015-16'),
    ('2016-17', '2016-17'),
)
MODULE_CODES = (
    ('MA0000','MA0000'),
    ('MA0003','MA0003'),
    ('MA1234','MA1234'),
    ('MA1501','MA1501'),
)


class Module(models.Model):

    # attributes
    year = models.CharField(max_length=6, choices=ACADEMIC_YEARS)
    code = models.CharField(max_length=7, choices=MODULE_CODES)
    title = models.CharField(max_length=100, null=True, blank=True)

    # users
    teacher = models.ForeignKey(User, null=True, blank=True, related_name="module_teacher")
    students = models.ManyToManyField(User, related_name="module_students")

    # misc
    twitter_widget_id = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.code

    @property
    def long_name(self):
        return "{} {} ({})".format(self.code, self.title, self.year)

    # def get_absolute_url(self):
    #     return reverse('module-detail', kwargs={'module_code': self.code})

    def get_absolute_url(self):
        #return reverse('module_detail', kwargs={'pk': self.id})

        #change to just ID
        return (self.id)

    def get_next(self):
        nesaf = Module.objects.filter(code__gt=self.code)
        if nesaf:
            return nesaf[0]
        return None

    def get_prev(self):
        prev = Module.objects.filter(code__lt=self.code).order_by('-code')
        if prev:
            return prev[0]
        return None


class BookNode(MPTTModel):

    # keys
    # module = models.ForeignKey(Module)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    # attributes
    node_class = models.CharField(max_length=10)
    node_type = models.CharField(max_length=10)
    number = models.PositiveSmallIntegerField(null=True) # latex number (chapter, figure etc)
    title = models.CharField(max_length=100, null=True, blank=False) # title or caption
    is_readonly = models.BooleanField(default=False)    # set by schedule.py (todo)

    # content
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='/media', null=True, blank=False)

    # labels
    node_id = models.PositiveSmallIntegerField()  # serial number (from booktree.py)
    mpath = models.CharField(max_length=100, null=True)  # materialized path (from booktree.py)
    label = models.CharField(max_length=100, null=True, blank=False)

    def get_absolute_url(self):
        return reverse('booknode_detail', kwargs={'pk': self.pk})

    def get_pretty_url(self):
        if self.node_type == "chapter":
            return reverse('module:chapter_detail', args=[self.pk])
        return self.get_absolute_url()

    def get_next(self, n_type=None):
        c = self
        while c.get_next_sibling():
            n = c.get_next_sibling()
            if not n_type or n.node_type == n_type:
                return n
            c = n
        return None

    def get_next_same_type(self):
        return self.get_next(self.node_type)

    def get_prev(self, n_type=None):
        c = self
        while c.get_previous_sibling():
            p = c.get_previous_sibling()
            if not n_type or p.node_type == n_type:
                return p
            c = p
        return None

    def get_prev_same_type(self):
        return self.get_prev(self.node_type)

    def get_siblings_by_type(self, n_type=None):
        return self.get_siblings(include_self=True).filter(node_type=n_type)

    def get_siblings_same_type(self):
        return self.get_siblings_by_type(self.node_type)

    def get_parent_by_type(self, node_type):
        """
        Get the closest parent node with the specified type
        If no parent with the correct type exists, return the
        root node
        :param node_type:
        :return: BookNode object
        """
        # pa = self.parent
        pa = self
        if not pa:
            # No parent - means we're the root
            return None
        while pa.node_type != node_type:
            if pa.is_root_node():
                return pa
            pa = pa.parent
        return pa

    def get_parent_book(self):
        """
        Get the first parent of this node of type book
        :return: BookNode object
        """
        return self.get_parent_by_type("book")

    def get_parent_chapter(self):
        """
        Get the first parent of this node of type chapter
        :return: BookNode object
        """
        return self.get_parent_by_type("chapter")

    def get_parent_assignment(self):
        pa = self
        while pa.node_class != 'assignment':
            pa = pa.parent
        return pa

    def get_root_node(self):
        """
        Proxy to MPTT builtin get_root
        """
        return self.get_root()

    def get_book(self):
        """
        Get the book object that this node is a child of
        :return: Book object
        """
        return self.get_root().book_set.first()

    def get_descendants_inc_self(self):
        return self.get_descendants(include_self=True)

    class MPTTMeta:
        order_insertion_by = ['node_id']

    def __str__(self):
        return self.mpath


class Book(models.Model):
    module = models.ForeignKey(Module, null=True, blank=True, related_name="book_set")
    number = models.PositiveSmallIntegerField(null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    new_commands = models.CharField(max_length=5000, null=True, blank=True)
    tree = models.ForeignKey(BookNode, related_name="book_set", null=True)

    def __str__(self):
        s = ''
        if self.module:
            s += self.module.code
        if self.number:
            s += ' | book ' + str(self.number)
        if self.title:
            s += ' | ' + self.title
        # if self.new_commands:
        #     s += '\n' + self.new_commands
        return unicode(s)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.id})

    def get_next(self):
        return self.module.book_set.filter(number__gt=self.number).first()

    def get_prev(self):
        return self.module.book_set.filter(number__lt=self.number).last()


class Label(models.Model):
    book = models.ForeignKey(Book)
    text = models.CharField(max_length=100)
    mpath = models.CharField(max_length=1000)

    def __str__(self):
        return u"{} -> {}".format(self.text, self.mpath)


class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(BookNode)
    text = models.TextField()
    is_readonly = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        base = u"{}|{}|{}".format(self.question.mpath, self.user.username, self.text)
        if self.is_readonly:
            base += u" (READONLY)"
        return base

class SingleChoiceAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(BookNode)
    choice = models.ForeignKey(BookNode, related_name='mcanswer_choice')
    is_readonly = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        s = self.question.mpath
        s = s + '|' + self.user.username
        s = s + '|' + str(self.choice)
        s = s + '|' + str(self.is_readonly) + '\n'
        return unicode(s)


class Submission(models.Model):
    user = models.ForeignKey(User)
    assignment = models.ForeignKey(BookNode)
    is_readonly = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

