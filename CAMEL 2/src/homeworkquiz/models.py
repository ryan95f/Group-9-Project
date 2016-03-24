from django.db import models

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

from user.models import CamelUser
from latexbook.models import BookNode


class Answer(models.Model):
    '''Current Student Answer - Allows for latex to be entered'''
    homework_node = models.ForeignKey(BookNode)
    user = models.ForeignKey(CamelUser)
    student_text = models.TextField()
    is_readonly = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.pk


class SingleChoiceAnswer(models.Model):
    '''Object to hold multiple choice answers'''
    user = models.ForeignKey(CamelUser)
    question = models.ForeignKey(BookNode)
    choice = models.ForeignKey(BookNode, related_name='mcanswer_choice')
    is_readonly = models.BooleanField(default=False)

    def __str__(self):
        return self.user.pk


class Submission(models.Model):
    '''Submission of SingleChoiceAnswer or Answer'''
    user = models.ForeignKey(CamelUser)
    assignment = models.ForeignKey(BookNode)
    is_readonly = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.pk

    class Meta:
        ordering = ['created']
