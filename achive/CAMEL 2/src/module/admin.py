from django.contrib import admin

from .models import LearningMaterial, Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    The representation of our Modules within Django's admin interface.

    This also allows for the user to add LearningMaterials to the selected Module.
    """


@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    """
    The representation of our LearningMaterials within Django's admin interface.

    This could possibly be improved upon, but is not a priority!
    """
