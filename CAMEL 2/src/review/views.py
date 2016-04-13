from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View

from latexbook.models import BookNode, Book
from homeworkquiz.models import SingleChoiceAnswer, JaxAnswer, MultiChoiceAnswer
from module.models import Module


class StaffRequiredMixin(object):
    """Object that allows staff access to the specific view.
    Displays error 403 if access not allowed"""

    def dispatch(self, request, *args, **kwargs):
        """Method that check current user has correct permission"""
        if not request.user.is_camel_staff:
            raise PermissionDenied
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class ReviewIndexView(StaffRequiredMixin, View):
    """View for review app that will display all modules that are stored in CAMEL.
    Implements the StaffRequiredMixin for security"""

    def get(self, request):
        """Method to get all modules and direct to template"""
        modules = Module.objects.all()
        return render(request, "review/index.html", {'modules': modules})


class ReivewBookIndex(StaffRequiredMixin, View):
    """View that will display all books for the module that was
    chosen from index. Only books for that module will be shown. Implements the
    StaffRequiredMixin for security"""

    def get(self, request, **kwargs):
        """Method to get books for the selected modue. If module
        does not exist then 404 will be displayed."""

        module = get_object_or_404(Module, pk=kwargs['module_pk'])
        learningmaterials = {}

        for learningmaterial in module.learningmaterial_set.all():
            material = learningmaterial.material_content_object
            learningmaterials.setdefault(material.__class__.__name__, []).append(material)

        return render(request, "review/book_index.html", {'learningmaterials': learningmaterials, 'module': module})


class ReviewBookView(StaffRequiredMixin, View):
    """View to display all questions that were in the selected
    book. Implements the StaffRequiredMixin for security"""

    def get(self, request, **kwargs):
        """Method to get the questions for the selected book. Finds
        root node then filters out all nodes that are not questions"""
        book = Book.objects.get(pk=kwargs['book_pk'])

        # use book and get its root note
        root = BookNode.objects.get(level=0, pk=book.book_root_node.pk).get_descendants()

        # from root filter out non-quizquestions
        questions = root.filter(node_type='quizquestion')
        return render(request, "review/questions_index.html", {
            'questions': questions,
            'book': book,
            'module_pk': kwargs['module_pk'],
            'review': True,
        })


class ReviewQuestionView(StaffRequiredMixin, View):
    """View to allow access to a question and see all answers
    that have been created to date for it. Implements the StaffRequiredMixin
    for security"""

    def get(self, request, **kwargs):
        """Method that will get the answers for a given question"""
        models = [SingleChoiceAnswer, JaxAnswer, MultiChoiceAnswer]
        question = BookNode.objects.get(pk=kwargs['question_pk'])

        # go through each model to see if any questions exist for it
        for m in models:
            student_answers = m.objects.all().filter(
                node=BookNode.objects.get(pk=kwargs['question_pk'])
            )

            # if answers found then break loop
            if(len(student_answers) > 0):
                break

        return render(request, "review/question.html", {
            'question': question,
            'answers': student_answers,
            'review': True,
            'module_pk': kwargs['module_pk'],
            'book_pk': kwargs['book_pk'],
        })
