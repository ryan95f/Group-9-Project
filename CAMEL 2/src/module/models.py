from django.db import models

from latexbook.models import Book
from module.options import ACADEMIC_YEARS, MODULE_CODES

# Create your models here.
class Module(models.Model):
    """A module."""
    code = models.CharField(primary_key=True, max_length=6, choices=MODULE_CODES)
    year = models.CharField(max_length=6, choices=ACADEMIC_YEARS)
    title = models.CharField(max_length=64)

    # We use ManyToMany as a Book could be in multiple modules and a module can
    # have multiple books.
    books = models.ManyToManyField(Book)

    def __str__(self):
    	# String when object requested
    	return self.code + " - " + self.title