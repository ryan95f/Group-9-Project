from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.detail import DetailView

from latexbook.models import BookNode


class BookNodeDetail(DetailView):
    """"""
    model = BookNode

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book = self.get_object()
        context["book"] = book
        context["chapters"] = book.tree.get_descendants().filter(node_type="chapter")
        return context


def show_test(request):
    return render_to_response("latexbook/test.html",
                          {"nodes": BookNode.objects.all()},
                          context_instance=RequestContext(request))
