from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import BookNode


class BookNodeDetailView(DetailView):
    """Displays a list of all the chapters for the passed book."""

    model = BookNode
    template_name = "latexbook/booknode_detail_view.html"

    def get_context_data(self, **kwargs):
        """Return context data for displaying the list of objects.."""
        context = super(BookNodeDetailView, self).get_context_data(**kwargs)

        book_node = self.get_object()
        context["book"] = book_node.book
        context["module_number"] = self.kwargs['module_pk']
        context["chapters"] = book_node.get_descendants().filter(node_type="chapter")

        return context


class BookNodeChapterDetailView(DetailView):
    """Displays the contents of the specified book chapter."""

    model = BookNode
    template_name = "latexbook/booknode_chapter_detail_view.html"

    def get_context_data(self, **kwargs):
        """Return context data for displaying the list of objects.."""
        context = super(BookNodeChapterDetailView, self).get_context_data(**kwargs)
        chapter = self.get_object()
        context["book"] = chapter.parent
        # .get_descendants(include_self=True) used to make it recurse and
        # ensure correct  object type (Do not change).
        context["chapter"] = chapter.get_descendants(include_self=True)
        return context


def show_test(request, module_pk):
    """A test view which displays all our BookNode objects."""
    return render(
        request,
        "latexbook/recurselatextree.html",
        {"root_node": BookNode.objects.all()}
    )
