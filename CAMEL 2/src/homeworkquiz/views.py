from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic import View

from django.utils import timezone
from django.utils.html import escape

from homeworkquiz.models import SingleChoiceAnswer, MultiChoiceAnswer, JaxAnswer, Deadline
from homeworkquiz.forms import DeadlineForm

from user.models import CamelUser
from latexbook.models import BookNode


class StaffRequiredMixin(object):
    """Object that allows staff access to the specific view.
    Displays error 403 if access not allowed"""

    def dispatch(self, request, *args, **kwargs):
        """Method that check current user has correct permission"""
        if not request.user.is_camel_staff:
            raise PermissionDenied
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


class DeadlineSetView(StaffRequiredMixin, FormView):
    """View to open form to add deadline to a booknode for
    a quizquestion."""
    form_class = DeadlineForm
    template_name = 'homeworkquiz/set_deadline.html'
    model = Deadline

    def get_initial(self, **kwargs):
        """Sets the form fields to have any existing data
        prior to rendering the template."""
        initial = super(DeadlineSetView, self).get_initial()
        try:
            a = self.model.objects.get(pk=BookNode.objects.get(pk=self.kwargs['pk']))
            initial['node'] = a.node.pk
            initial['date'] = a.deadline_date
        except self.model.DoesNotExist:
            initial['node'] = self.kwargs['pk']
        return initial

    def form_valid(self, form):
        """Method that is executed when form that is send to back-end
        meets the requirements proposed by the corrisponding form. Creates
        or edits a Deadline object to add it to DB."""
        clean_form = form.clean_form()
        try:
            saved_deadline_object = self.model.objects.get(pk=clean_form['node'])
            saved_deadline_object.deadline_date = clean_form['date']
            saved_deadline_object.save()
        except self.model.DoesNotExist:
            deadline_object = self.model(
                node=BookNode.objects.get(pk=clean_form['node']),
                deadline_date=clean_form['date']
            )
            deadline_object.save()
        return HttpResponseRedirect(
            reverse('module:latexbook:booknode_chapter_detail',
                    args=(
                        self.kwargs["module_pk"],
                        self.kwargs['book_pk'],
                        self.kwargs['chapter_pk']),
                    )
        )

    def get_context_data(self, **kwargs):
        """Return context data for requested template"""
        context = super(DeadlineSetView, self).get_context_data(**kwargs)
        context['question'] = BookNode.objects.get(pk=self.kwargs['pk']).get_descendants(include_self=True)
        context["module_number"] = self.kwargs["module_pk"]
        context['question_number'] = self.kwargs['pk']
        context["book_number"] = self.kwargs["book_pk"]
        context["chapter_number"] = self.kwargs["chapter_pk"]
        context["deadline"] = True
        return context


class QuestionDetailView(DetailView):
    """View for loading the question that the user wishes
    to view, and will load any answers that have been stored
    previously"""

    model = BookNode
    template_name = "homeworkquiz/question_detail.html"

    def get_context_data(self, **kwargs):
        """Return context data for displaying the list of objects."""
        answer_models = [JaxAnswer, SingleChoiceAnswer, MultiChoiceAnswer]
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        node = self.get_object()
        context["module_number"] = self.kwargs["module_pk"]
        context["book_number"] = self.kwargs["book_pk"]
        context["chapter_number"] = self.kwargs["chapter_pk"]
        context["chapter"] = node.get_descendants(include_self=True)
        context["show"] = True

        # find the relevent model to display
        for m in answer_models:
            try:
                result = m.objects.get(
                    user=CamelUser.objects.get(identifier=self.request.user.identifier),
                    node=BookNode.objects.get(pk=node.pk)
                )
                context['previous_answer'] = result
            except m.DoesNotExist:
                pass

        try:  # find if a deadline has been set for this node
            deadline = Deadline.objects.get(pk=BookNode.objects.get(pk=node.pk))
            context['deadline'] = deadline.deadline_date
            # compare the dates last to get most accuare time of load
            context['late'] = (timezone.now() > deadline.deadline_date)
        except Deadline.DoesNotExist:
            context['deadline'] = None
        return context


class GeneralSave(object):
    '''General class that will save the answers that have been entered
    by the user. Takes in the model and answer to make the update'''

    def __init__(self, model, answer):
        """Constructor for GeneralSave object, takes model and answer"""
        self._model = model
        self._answer = answer

    def save_answer(self, request, node_pk):
        """Method to save the answer for the model that has been passed.
        if there has not been a attempt previously, then will create the
        object."""
        try:
            # use existing object to save if found
            current_answer = self._model.objects.get(
                user=CamelUser.objects.get(identifier=request.POST['user']),
                node=BookNode.objects.get(pk=node_pk)
            )
            current_answer.answer = self._answer
            current_answer.save_date = timezone.now()
            current_answer.save()
        except self._model.DoesNotExist:
            # create new object if not found
            current_answer = self._model(
                answer=self._answer,
                user=CamelUser.objects.get(identifier=request.POST['user']),
                node=BookNode.objects.get(pk=node_pk)
            )
            current_answer.save()
        return current_answer

    def submit_answer(self, submitModel):
        """Method to submit answer when answer object is provided"""
        submitModel.is_submitted = True
        submitModel.submitted_date = timezone.now()
        submitModel.save()
        return submitModel


class SingleChoiceSaveView(View):
    """View to save an redirect after answer has been saved or
    submitted. Used in Ajax requests (for save). Assumes if not
    ajax then submit. """

    def post(self, request, **kwargs):
        """Method executed when POST request is made to view"""
        s = GeneralSave(SingleChoiceAnswer, request.POST['singlechoice'].strip())
        single_model = s.save_answer(request, self.kwargs['node_pk'])
        if(request.is_ajax()):
            return JsonResponse({'singlechoice': single_model.answer})
        else:
            s.submit_answer(single_model)
        return HttpResponseRedirect(
            reverse('module:latexbook:booknode_chapter_detail',
                    args=(
                        self.kwargs["module_pk"],
                        self.kwargs['book_pk'],
                        self.kwargs['chapter_pk']),
                    )
        )


class MultiChoiceSave(View):
    """View to save an redirect after multi-choice answer has been saved or
    submitted. Used in Ajax requests (for save). Assumes if not
    ajax then submit. """

    def post(self, request, **kwargs):
        """Method executed when POST request is made to view"""
        if(request.is_ajax()):
            # ajax request automatically adds [] when entered
            answers = request.POST.getlist('multiplechoice[]')
        else:
            answers = request.POST.getlist('multiplechoice')

        # clean array so that it can be saved
        clean_answer = ''
        for ans in answers:
            clean_answer += ans + ','

        s = GeneralSave(MultiChoiceAnswer, clean_answer)
        # save answer
        multi_model = s.save_answer(request, self.kwargs['node_pk'])
        if(request.is_ajax()):
            return JsonResponse({'multiplechoice': multi_model.answer})
        else:
            s.submit_answer(multi_model)
            pass
        return HttpResponseRedirect(
            reverse('module:latexbook:booknode_chapter_detail',
                    args=(
                        self.kwargs["module_pk"],
                        self.kwargs['book_pk'],
                        self.kwargs['chapter_pk']),
                    )
        )


class JaxSaveView(View):
    """View to save an redirect after jax answer has been saved or
    submitted. Used in Ajax requests (for save). Assumes if not
    ajax then submit. """

    def post(self, request, **kwargs):
        """Method executed when POST request is made to view"""
        clean_jax = escape(request.POST['jax_answer'])
        s = GeneralSave(JaxAnswer, clean_jax)
        jax_object = s.save_answer(request, self.kwargs['node_pk'])
        if(request.is_ajax()):
            return JsonResponse({'jax_answer': clean_jax})
        else:
            s.submit_answer(jax_object)
        return HttpResponseRedirect(
            reverse('module:latexbook:booknode_chapter_detail',
                    args=(
                        self.kwargs["module_pk"],
                        self.kwargs['book_pk'],
                        self.kwargs['chapter_pk']),
                    )
        )
