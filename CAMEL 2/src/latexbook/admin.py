from django.contrib import admin

from .models import Module, BookNode, TextNode, Book

admin.site.register(Module)
admin.site.register(BookNode)
admin.site.register(TextNode)
admin.site.register(Book)
