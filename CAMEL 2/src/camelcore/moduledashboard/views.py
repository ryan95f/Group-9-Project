from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from latexbook.forms import LatexBookForm
from module.models import LearningMaterial, Module


def book_create_view(request, **kwargs):
    """View used to create a new book and upload it as a learning material.

    This must be improved upon massively! No verifications are yet performed.
    It would also be neat if we can offer the ability of selecting an already existing learning material book.
    """
    module = get_object_or_404(Module, pk=kwargs["module_pk"])
    if request.method == "POST":
        latex_book_form = LatexBookForm(request.POST, request.FILES)
        if latex_book_form.is_valid():
            new_book = latex_book_form.save()

            learning_material = LearningMaterial(material_content_object=new_book)

            # Instance requires a primary key value before a many-to-many relationship can be used, so we must save
            # the model instance first!
            learning_material.save()
            learning_material.modules.add(module)
            return HttpResponseRedirect("/")
    else:
        latex_book_form = LatexBookForm()
    return render(request, "camelcore/moduledashboard/book_create_form_view.html", {
        "form": latex_book_form
    })
