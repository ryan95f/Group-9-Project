from django.http import HttpResponseRedirect
from django.shortcuts import render

from latexbook.forms import BookForm, BookNodeForm


def book_create_view(request, **kwargs):
    """View used to create a new book and upload it as a learning material."""
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        node_form = BookNodeForm(request.POST, request.FILES)
        if book_form.is_valid() and node_form.is_valid():
            book_node = node_form.save()
            book_form.data["book_root_node"] = book_node
            book_form.save()
            return HttpResponseRedirect("/")
    else:
        book_form = BookForm()
        node_form = BookNodeForm()
    return render(request, "latexbook/book_create_form_view.html", {
        "book_form": book_form,
        "node_form": node_form
    })
