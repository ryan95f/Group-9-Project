from django.contrib import admin

from .models import BookNode, TextNode, Book

admin.site.register(BookNode)
admin.site.register(TextNode)
admin.site.register(Book)
