from django.shortcuts import render

# model-based views
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from core.models import Module, Book, BookNode

class Module_ListView(ListView):
    model = Module
    context_object_name = "module_list"
    template_name = 'module/module_list.html'
    queryset = Module.objects.order_by('year','code')


class Module_DetailView(DetailView):
    model = Module
    template_name = 'module/module_detail.html'

    def get_context_data(self, **kwargs):
        context = super(Module_DetailView, self).get_context_data(**kwargs)
        module = self.get_object()
        context['module'] = module
        context['books'] = module.book_set.all().order_by('number')
        context['next'] = module.get_next()
        context['prev'] = module.get_prev()
        context['toc'] = Module.objects.all().order_by('code')
        return context

class Book_DetailView(DetailView):
    model = Book
    template_name = 'module/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super(Book_DetailView, self).get_context_data(**kwargs)
        book = self.get_object()
        context['book'] = book
        context['module'] = book.module
        context['chapters'] = book.tree.get_descendants().filter(node_type="chapter")
        context['next'] = book.get_next()
        context['prev'] = book.get_prev()
        context['toc'] = book.module.book_set.all().order_by('number')
        return context

class Chapter_DetailView(DetailView):
    model = BookNode
    template_name = 'module/chapter_detail.html'

    def get_context_data(self, **kwargs):
        context = super(Chapter_DetailView, self).get_context_data(**kwargs)
        chapter = self.get_object()
        context['module'] = chapter.get_book().module
        context['book']  = chapter.get_book()
        context['chapter'] = chapter
        context['subtree'] = chapter.get_descendants(include_self=True)
        context['toc'] = chapter.get_siblings(include_self=True)
        return context

class BookNode_DetailView(DetailView):
	####
	# I think this is not used
	###
    model = BookNode
    template_name = 'booknode_detail.html'
    # def get_success_url(self):
    #     return reverse('chapter-list')
    def get_context_data(self, **kwargs):
        context = super(BookNode_DetailView, self).get_context_data(**kwargs)
        subtree = self.get_object().get_descendants(include_self=True)
        module = self.get_object().get_book().module
        context['module'] = module
        context['subtree'] = subtree
        chapter = self.get_object().get_parent_chapter()
        context['chapter'] = chapter
        context['toc'] = module.book_set.all()
        context['next'] = self.get_object().get_next()
        context['prev'] = self.get_object().get_prev()
        return context


def selected(request, pk, node_type):
	# used to choose type of page
	# e.g Homework, Test, Figures
    context = {}
    booknode = BookNode.objects.get(pk=pk)
    module = booknode.get_book().module
    chapter = booknode.get_parent_chapter()

    context['module'] = module
    context['chapter'] = chapter
    context['book'] = chapter.get_book()
    context['user'] = request.user

    context['node_type'] = node_type

    chapter_items = chapter.get_descendants()
    if node_type == 'theorem':
        qset = chapter_items.filter(node_class="theorem").exclude(node_type__in=['example', 'exercise'])
    elif node_type == 'test':
        qset = chapter_items.filter(node_type__in=['singlechoice', 'multiplechoice'])
    else:
        qset = chapter_items.filter(node_type=node_type)
    context['booknodes'] = qset.order_by('mpath')

    context['next'] = chapter.get_next()
    context['prev'] = chapter.get_prev()
    context['toc'] = BookNode.objects.filter( node_type="chapter", mpath__startswith=module.code).order_by('mpath')
    return render(request, 'module/chapter_selected_nodes.html', context)
