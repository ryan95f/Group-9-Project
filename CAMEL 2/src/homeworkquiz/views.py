from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.views.generic.detail import DetailView
from django.views.generic import View

from django.utils import timezone
from django.utils.html import escape

from homeworkquiz.models import SingleChoiceAnswer, JaxAnswer
from user.models import CamelUser
from latexbook.models import BookNode


def save_answer(request, node_pk):
    """ temp function, placeholder view for unimplemented questions
    currently in use for Multi answers"""
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class QuestionDetailView(DetailView):
    """View for loading the question that the user wishes
    to view, and will load any answers that have been stored
    previously"""

    model = BookNode
    template_name = "homeworkquiz/question_detail.html"

    def get_context_data(self, **kwargs):
        """Return context data for displaying the list of objects."""
        answer_models = [JaxAnswer, SingleChoiceAnswer]
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        node = self.get_object()
        context["chapter"] = node.get_descendants(include_self=True)
        context["show"] = True

        for m in answer_models:
            try:
                result = m.objects.get(
                    user=CamelUser.objects.get(identifier=self.request.user.identifier),
                    node=BookNode.objects.get(pk=node.pk)
                )
                context['previous_answer'] = result
            except m.DoesNotExist:
                pass
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
    """View to save an redirect after answer has been saved and
    submitted. Used in Ajax requests (for save). Assumes if not
    ajax then submit. """

    def post(self, request, node_pk):
        """Method executed when POST request is made to view"""
        s = GeneralSave(SingleChoiceAnswer, request.POST['singlechoice'].strip())
        single_model = s.save_answer(request, node_pk)
        if(request.is_ajax()):
            return JsonResponse({'singlechoice': single_model.answer})
        else:
            s.submit_answer(single_model)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# cannot complete this one until check boxes are used for multiple choice
# class MultiChoiceSave(View):
#     def post(self, request, node_pk):
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class JaxSaveView(View):
    """View to save an redirect after jax answer has been saved and
    submitted. Used in Ajax requests (for save). Assumes if not
    ajax then submit. """

    def post(self, request, node_pk):
        """Method executed when POST request is made to view"""
        clean_jax = escape(request.POST['jax_answer'])
        s = GeneralSave(JaxAnswer, clean_jax)
        jax_object = s.save_answer(request, node_pk)
        if(request.is_ajax()):
            return JsonResponse({'jax_answer': clean_jax})
        else:
            s.submit_answer(jax_object)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
