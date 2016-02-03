from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.detail import DetailView

from .models import BookNode, Book


class BookNodeDetailView(DetailView):
    """Displays a list of all the chapters for the passed book."""
    model = BookNode
    template_name = "latexbook/booknode_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(BookNodeDetailView, self).get_context_data(**kwargs)
        book_node = self.get_object()
        context["book"] = book_node.book
        context["chapters"] = book_node.get_descendants().filter(node_type="chapter")
        return context


class BookNodeChapterDetailView(DetailView):
    """Displays the contents of the specified book chapter."""
    model = BookNode
    template_name = "latexbook/booknode_chapter_detail_view.html"

    def get_context_data(self, **kwargs):
        context = super(BookNodeChapterDetailView, self).get_context_data(**kwargs)
        chapter = self.get_object()    
        context["book"] = chapter.parent # == <class 'latexbook.models.BookNode'> not MPTT format
        context["chapter"] = chapter # == <class 'latexbook.models.BookNode'> not the correct MPTT Format
        context['root'] = BookNode.objects.all()
        return context


def show_test(request, module_pk):
    #http://127.0.0.1:8000/module/MA0000/test/ 

    #print(type(BookNode.objects.get(pk=1))) == <class 'latexbook.models.BookNode'>
    print(type(BookNode.objects.all())) # == <class 'mptt.querysets.TreeQuerySet'>( we want this )
    # shows the effect 

    # return render(
    #     request,
    #     "latexbook/recurselatextree.html",
    #     {"root_node": BookNode.objects.get(pk=1)}
    # )

    return render(
        request,
        "latexbook/recurselatextree.html",
        {"root_node": BookNode.objects.all()}
    )
