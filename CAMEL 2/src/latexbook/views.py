from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.detail import DetailView

from .models import BookNode


class BookNodeDetailView(DetailView):
    """Displays a list of all the chapters for the passed book."""
    model = BookNode
    template_name = "latexbook/booknode_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(BookNodeDetailView, self).get_context_data(**kwargs)
        book = self.get_object()
        context["book"] = book
        context["chapters"] = book.get_descendants().filter(node_type="chapter")
        return context


class BookNodeChapterDetailView(DetailView):
    """Displays the contents of the specified book chapter."""
    model = BookNode
    template_name = "latexbook/booknode_chapter_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(BookNodeChapterDetailView, self).get_context_data(**kwargs)
        chapter = self.get_object()
        context["book"] = chapter.parent
        context["chapter"] = chapter
        return context


def show_test(request):
    return render(
        request,
        "latexbook/recurselatextree.html",
        {"root_node": BookNode.objects.all()}
    )
