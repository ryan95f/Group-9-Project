from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
from latexbook.models import BookNode
from user.models import CamelUser

# We shouldn't be directly importing any of our other apps.
# It contradicts the fact that our apps are meant to be decoupled; a point we have fairly emphasised throughout our
# reports.
# Each one of our project's apps - except camelcore - should be integratable into other Django projects.
# This requires us to focus on two things:
# - Do not create dependencies with other apps (unless the alternative makes absolutely no sense).
# - Make relations generic where necessary.
#
# If we stick with the Django mindset of reusability & decoupled apps, we'll probably have to modify the user app as
# it holds a dependecy with Camel. Maybe we should leave the user app purely for its login/logout functionality
# and some additional user fields. All the staff related stuff should only exist within the camelcore app. I think
# it'll also be a neat idea if the homeworkquiz app would define the permissions for being able to create tests etc...
#
# Also, whilst I'm typing here, if you get a spare few minutes, would you mind taking a look at:
# 'CAMEL 2/src/latexbook/templatetags/latex_html.py :: get_template_node(...)'
# I wanted:
# 'CAMEL 2/src/camel2/templates/camelcore/homeworkquiz/latexbook/latexparser/nodes/commands/choice/correctchoice.html'
# to simply extend from:
# 'CAMEL 2/src/camel2/templates/camelcore/homeworkquiz/latexbook/latexparser/nodes/commands/choice/choice.html'
# But it was just giving me a fuck load of errors.
#
# Django's contenttypes framework is quite handy for this kind of stuff! :)
# https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/


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
    node = models.OneToOneField(BookNode, default=None, primary_key=True)
    deadline_date = models.DateTimeField(auto_now_add=False)
