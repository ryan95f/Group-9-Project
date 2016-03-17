from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from module.options import ACADEMIC_YEARS


# Create your models here.
class Module(models.Model):
    """A module which users can be enrolled upon."""

    code = models.CharField(primary_key=True, max_length=7)
    year = models.CharField(max_length=7, choices=ACADEMIC_YEARS)
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.code + " - " + self.title


class LearningMaterial(models.Model):
    """
    Associates learning materials to our modules.

    As a learning material could be of various types, we utilise Django's Content Types framework.

    For more infomration:
    https://docs.djangoproject.com/en/1.9/ref/contrib/contenttypes/
    """

    # The Modules associated with this learning material
    modules = models.ManyToManyField(Module)

    # The content of this learning material
    material_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    material_object_id = models.PositiveIntegerField()
    material_content_object = GenericForeignKey('material_content_type', 'material_object_id')

    def __str__(self):
        modules_str = "[" + ", ".join([str(m) for m in self.modules.all()]) + "]"
        return str(self.material_content_object) + " - " + modules_str
