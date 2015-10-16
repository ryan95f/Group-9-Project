"""
camel: admin.py
"""
from django.contrib import admin

from core.models import (
    Module, Book, BookNode, Label, Answer, SingleChoiceAnswer, Submission
)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'email')
    ordering = ('username',)


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('code', 'year', 'title',)
    ordering = ('code', 'year',)


class BookAdmin(admin.ModelAdmin):
    list_display = ('module', 'tree', 'number', 'title', 'author', 'version',)
    ordering = ('module', 'tree',)


class BookNodeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'mpath',
        'node_class',
        'node_type',
        'label',
        'number',
        'title',
        'text',
        'image')
    ordering = ('mpath',)


class LabelAdmin(admin.ModelAdmin):
    list_display = ('text', 'mpath')
    ordering = ('mpath', 'text')


class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'question',
        'user',
        'text',
        'is_readonly',
        'created',
        'updated')
    ordering = ('question', 'user')


class SingleChoiceAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'question',
        'user',
        'choice',
        'is_readonly',
        'created',
        'updated')
    ordering = ('question', 'user')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'assignment', 'user', 'created',)
    ordering = ('created', 'user')

admin.site.register(Module, ModuleAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookNode, BookNodeAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(SingleChoiceAnswer, SingleChoiceAnswerAdmin)
admin.site.register(Submission, SubmissionAdmin)
