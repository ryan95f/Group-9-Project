from django.db import models

from latexbook.models import BookNode
from user.models import CamelUser


class GenericAnswerModel(models.Model):
    """Concrate model that contains the core variables
    for storing a students answer. Is inherited to allow
    other specific models access."""
    user = models.ForeignKey(CamelUser, default=None)
    node = models.ForeignKey(BookNode, default=None)
    created = models.DateTimeField(auto_now_add=True)
    save_date = models.DateTimeField(auto_now=True)
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_submitted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def question_node_id(self):
        return self.node.pk


class SingleChoiceAnswer(GenericAnswerModel):
    """Model for holding the data that is related
    to an answer that is entered by a user for Single Choice.
    Inherits GenericAnswerModel which contains core information"""
    answer = models.CharField(max_length=20)

    def __str__(self):
        return self.answer


class JaxAnswer(GenericAnswerModel):
    """Model for holding the answer that is entered
    for a mathjax answer. Inherits GenericAnswerModel which
    contains core information"""
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.answer


class MultiChoiceAnswer(GenericAnswerModel):
    """Model for holding the answer that is entered
    for a multiple choice answer. Inherits GenericAnswerModel which
    contains core information"""
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.answer


class Deadline(models.Model):
    """Model to hold the deadline that for a given question. Requires node wrapper
    and a deadline to create this object"""
    node = models.OneToOneField(BookNode, default=None, primary_key=True)
    deadline_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.deadline_date

    def node_pk(self):
        """Method to return primary key of node"""
        return self.node.pk
