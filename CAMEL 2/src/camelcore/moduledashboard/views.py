from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from latexbook.forms import BookForm, BookNodeForm
from module.models import LearningMaterial, Module


def book_create_view(request, **kwargs):
    """View used to create a new book and upload it as a learning material.

    This must be improved upon massively! No verifications are yet performed.
    It would also be neat if we can offer the ability of selecting an already existing learning material book.
    """
    module = get_object_or_404(Module, pk=kwargs["module_pk"])
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        node_form = BookNodeForm(request.POST, request.FILES)
        if book_form.is_valid() and node_form.is_valid():
            book_node = node_form.save()

            new_book = book_form.save(commit=False)
            new_book.book_root_node = book_node
            new_book.save()

            learning_material = LearningMaterial()
            learning_material.material_content_object = new_book

            # Instance requires a primary key value before a many-to-many relationship can be used.
            # So we must save the model instance first!
            learning_material.save()
            learning_material.modules.add(module)
            return HttpResponseRedirect("/")
    else:
        book_form = BookForm()
        node_form = BookNodeForm()
    return render(request, "camelcore/moduledashboard/book_create_form_view.html", {
        "book_form": book_form,
        "node_form": node_form
    })
