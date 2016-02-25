from django.db import models
from django.contrib.auth.models import User

from latexbook.models import BookNode

class Answer(models.Model):
	'''Current Student Answer - Allows for latex to be entered'''
	homework_node = models.ForeignKey(BookNode)
	user = models.ForeignKey(User)
	student_text = models.TextField()
	is_readonly = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return user.pk

class SingleChoiceAnswer(models.Model):
	'''Object to hold multiple choice answers'''
	user = models.ForeignKey(User)
	question = models.ForeignKey(BookNode)
	choice = models.ForeignKey(BookNode, related_name='mcanswer_choice')
	is_readonly = models.BooleanField(default=False)

	def __str__(self):
		return user.pk

class Submission(models.Model):
	'''Submission of SingleChoiceAnswer or Answer'''
	user = models.ForeignKey(User)
	assignment = models.ForeignKey(BookNode)
	is_readonly = models.BooleanField(default=True)

	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return user.pk

	class Meta:
		ordering = ['created']
