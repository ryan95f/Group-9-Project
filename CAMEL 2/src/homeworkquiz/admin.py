from django.contrib import admin
from homeworkquiz.models import SingleChoiceAnswer, JaxAnswer, MultiChoiceAnswer, Deadline


class AnswerAdmin(admin.ModelAdmin):
    """Model for answers to be displayed in Django Admin panel. Applied t
    all answers types. Restricts what can be edited by Admin"""
    list_display = ('user', 'created', 'question_node_id', 'is_submitted')
    list_filter = ('is_submitted', 'created')
    fieldsets = (
        ('User Answer', {'fields': ('answer',)}),
        ('Permissions', {'fields': ('is_submitted',)}),
    )


class DeadlineAdmin(admin.ModelAdmin):
    """Model for deadlines to be displayed on the Django admin panel.
    Used only for the Deadline model"""
    list_display = ('node', 'node_pk', 'deadline_date', )

admin.site.register(SingleChoiceAnswer, AnswerAdmin)
admin.site.register(JaxAnswer, AnswerAdmin)
admin.site.register(MultiChoiceAnswer, AnswerAdmin)
admin.site.register(Deadline, DeadlineAdmin)
