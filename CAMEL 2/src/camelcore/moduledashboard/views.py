from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from latexbook.forms import LatexBookForm
from latexbook.models import Book
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


def book_delete_view(request, **kwargs):
    """Delete the Book LearningMaterial for the given Module.

    If no other Modules use this Book, it is deleted entirely.
    """
    module = get_object_or_404(Module, pk=kwargs["module_pk"])
    book = get_object_or_404(Book, pk=kwargs["book_pk"])

    book_object_type = ContentType.objects.get_for_model(Book)
    learning_material = LearningMaterial.objects.filter(
        material_content_type__pk=book_object_type.id,
        material_object_id=book.pk,
    ).first()

    learning_material.modules.remove(module)

    if learning_material.modules.count() == 0:
        learning_material.delete()  # Book delete can't cascade
        book.delete()

    return HttpResponseRedirect("/")
