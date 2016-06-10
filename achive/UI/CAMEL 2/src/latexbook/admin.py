from django.contrib import admin

from .models import Book, BookNode, TextNode

admin.site.register(BookNode)
admin.site.register(TextNode)
admin.site.register(Book)
