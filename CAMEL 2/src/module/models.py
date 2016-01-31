from django.db import models

from latexbook.models import Book


# Create your models here.
class Module(models.Model):
    """A module."""

    code = models.CharField(primary_key=True, max_length=6)

    title = models.CharField(max_length=64)

    # We use ManyToMany as a Book could be in multiple modules and a module can
    # have multiple books.
    books = models.ManyToManyField(Book)