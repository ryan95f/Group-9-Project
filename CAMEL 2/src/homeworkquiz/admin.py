from django.contrib import admin
from homeworkquiz.models import SingleChoiceAnswer, JaxAnswer


class AnswerAdmin(admin.ModelAdmin):
    """Model for answers to be displayed in Django Admin panel. Applied t
    all answers types. Restricts what can be edited by Admin"""
    list_display = ('user', 'created', 'question_node_id', 'is_submitted')
    list_filter = ('is_submitted', 'created')
    fieldsets = (
        ('User Answer', {'fields': ('answer',)}),
        ('Permissions', {'fields': ('is_submitted',)}),
    )

admin.site.register(SingleChoiceAnswer, AnswerAdmin)
admin.site.register(JaxAnswer, AnswerAdmin)
