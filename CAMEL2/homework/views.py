from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic import View

from core.models import BookNode, Answer, Submission, SingleChoiceAnswer
from django.contrib.auth.models import User
from homework.forms import UserForm, AnswerForm, SubmissionForm, BookNode


''' Start of code that relates to edit_answer.html '''

# edit answer form
class Edit_Answer(View):

    def get(self, request, pk):
        '''
        Method use to create page when requested by the user
        via URL.
        '''
        context = {}
        qu = BookNode.objects.get(pk=pk)
        context['module'] = qu.get_book().module
        context['book'] = qu.get_book()
        context['question'] = qu
        context['subtree'] = qu.get_descendants(include_self=True)
        context['chapter'] = qu.get_parent_chapter()
        assignment = qu.get_parent_assignment()
        context['assignment'] = assignment
        context['toc'] = qu.get_siblings(include_self=True)

        # navigation
        questions = assignment.get_descendants().filter(node_type="question").order_by('mpath')
        next = questions.filter( mpath__gt=qu.mpath )
        prev = questions.filter( mpath__lt=qu.mpath ).order_by('-pk')
        context['next'] = next[0] if next else None
        context['prev'] = prev[0] if prev else None

        try:
            ans = Answer.objects.get(question=qu, user=request.user)
            form = AnswerForm(instance=ans)
        except Answer.DoesNotExist:
            form = AnswerForm(initial={'question': qu, 'user': request.user})
            
        context['form'] = form
        return render(request, 'homework/edit_answer.html', context)

    def post(self, request, pk):
        '''
        Method use to either save then exit the form along with
        saving the contents of the box. Or Exit completly 
        to go back to the homework page.
        '''
        context = {}
        form = AnswerForm(request.POST)
        if form.is_valid():
            ques = form.cleaned_data['question']
            user = form.cleaned_data['user']

            # search for saved answer
            answer = Answer.objects.filter(question=ques, user=user).first()

            # create new answer if required
            if not answer:
                answer = form.save(commit=False)
                answer.save()

            elif 'save-and-exit' in request.POST:
                ''' save the current answer then go to previous page '''
                answer.text = form.cleaned_data['text']
                answer.is_readonly = form.cleaned_data['is_readonly']
                answer.save()
                return HttpResponseRedirect( reverse('homework:homework', kwargs={'pk': ques.get_parent_assignment().id}) )
            elif 'exit' in request.POST:
                return HttpResponseRedirect( reverse('homework:homework', kwargs={'pk': ques.get_parent_assignment().id}) )
            else:
                print ("BAD LUCK")
        else:
            print ("FORM INVALID")
            context['debug'] = form.errors

        context['form'] = form
        return render(request, 'homework/edit_answer.html', context)

class Edit_Answer_Ajax(View):
    '''
    Contains function that soley is used for Ajax request
    for edit_answer.html. Takes the user data if exist and update.
    Exception occurs when new answer is being created via Ajax.
    '''

    def post(self, request, pk):
        # Ajax method
        ques = request.POST['question']
        user = request.POST['user']
        try:
            # editing a old answer
            answer = Answer.objects.filter(question=ques, user=user).first()
            answer.text = request.POST['text']
            answer.is_readonly = False
        except:
            # create a new answer
            # instances of the User and Node need to 
            # be created to prevent attribute errors
            user_instance = User.objects.get(pk=user)
            node_instance = BookNode.objects.get(pk=ques)
                
            # creating the new answer submission
            answer = Answer(question=node_instance, user=user_instance)
            answer.text = request.POST['text']
            answer.is_readonly = False
            
        answer.save()
        return JsonResponse({'out_text' : answer.text,})

''' End of code that relates to edit_answer.html '''



# homework (question set)
class Homework(View):
    def get(self,request, pk):
        context = {}
        hwk = BookNode.objects.get(pk=pk)
        context['module'] = hwk.get_book().module
        context['homework'] = hwk

        chapter = hwk.get_parent_chapter()
        context['chapter'] = chapter
        context['book'] = hwk.get_book()
        homeworks = chapter.get_descendants().filter(node_type="homework").order_by('mpath')
        context["toc"] = homeworks

        # navigation
        next = homeworks.filter( mpath__gt=hwk.mpath )
        prev = homeworks.filter( mpath__lt=hwk.mpath ).order_by('-mpath')
        context['nnext'] = next[0] if next else None
        context['prev'] = prev[0] if prev else None

        questions = BookNode.objects.filter(node_type='question', mpath__startswith=hwk.mpath).order_by('mpath')
        context['questions'] = questions
        answers = []

        # create question-answer pairs (answer=None is not yet attempted/saved)
        for qu in questions:
            answers.append( Answer.objects.filter(user=request.user, question=qu).first() )
        context['answers'] = answers
        pairs = zip(questions,answers)
        context['pairs'] = pairs

        # check whether this homework has already been submitted
        sub = Submission.objects.filter(user=request.user, assignment=hwk).first()
        if sub:
            context['submission'] = sub

        # submit form: hitch on hidden fields here
        form = SubmissionForm( initial={'user': request.user, 'assignment':hwk.pk, 'declaraion': False} )
        form.fields['answers'] = answers
        context['form'] = form

        return render(request,'homework/homework.html', context)

    def post(self, request, pk):
        ''' Method is used to save the student answers to the database 
        and prevent them from editing them. '''

        answers = []
        context = {}
        hwk = BookNode.objects.get(pk=pk)
        form = SubmissionForm(request.POST)
        if form.is_valid():
            if 'submit-homework' in request.POST:
                questions = BookNode.objects.filter(node_type='question', mpath__startswith=hwk.mpath).order_by('mpath')
                for qu in questions:
                    answers.append( Answer.objects.filter(user=request.user, question=qu).first() )
                    context['answers'] = answers
                submission = form.save(commit=False)
                submission.save()
                # for answer in form.cleaned_data['answers']:
                for answer in answers:
                    if answer:
                        answer.submission = submission
                        answer.is_readonly = True
                        answer.save()
            return HttpResponseRedirect( reverse('homework:homework', kwargs={'pk': hwk.id}) )
        else:
            context['debug'] = form.errors
            return render(request,'core/index.html', context)




''' !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '''
# single choice test
''' Has to be finished as inital project did not have this function completed '''
@login_required
def sctest(request, pk):
    context = {}
    test = BookNode.objects.get(pk=pk)
    chapter = test.get_parent_chapter()
    questions = BookNode.objects.filter(node_type='question', mpath__startswith=test.mpath).order_by('mpath')

    context['module'] = chapter.get_book().module
    context['test'] = test
    context['chapter'] = chapter
    context['questions'] = questions
    context['book']  = chapter.get_book()
    context['toc'] = BookNode.objects.filter( node_type="homework", mpath__startswith=chapter.mpath ).order_by('mpath')

    # navigation
    tests = BookNode.objects.filter( node_type__in=['singlechoice','multiplechoice'], mpath__startswith=chapter.mpath ).order_by('mpath')
    next = tests.filter( mpath__gt=test.mpath )
    prev = tests.filter( mpath__lt=test.mpath ).order_by('-mpath')
    context['next'] = next[0] if next else None
    context['prev'] = prev[0] if prev else None

    triplets = []

    # create question-choices-answer triplets (answer=None is not yet attempted)
    for qu in questions:
        choices = BookNode.objects.filter( node_type__in=['choice','correctchoice'], mpath__startswith=qu.mpath)
        answer = SingleChoiceAnswer.objects.filter(user=request.user, question=qu).first() # returns none if not yet attempted
        triplets.append([ qu, choices, answer])

    context['triplets'] = triplets

    # check whether this homework has already been attempted
    submission = Submission.objects.filter(user=request.user, assignment=test).first()
    if submission:
        context['submission'] = submission

    # form: hitch on hidden fields here
    form = SubmissionForm( initial={'user': request.user, 'assignment':test.pk} )
    context['form'] = form

    if request.method == 'POST':
        # deal with form (submit)
        # print request.POST
        form = SubmissionForm(request.POST)
        if form.is_valid():

            # extract chosen answers through raw post data (oops!)
            pairs = dict([ [int(k.split('_')[1]),int(v.split('_')[1])] for k,v in form.data.items() if k[:9] == 'question_'])
            for trip in triplets:
                qu = trip[0]
                ch = trip[1]
                an = trip[2]
                if qu.number in pairs:
                    chno = pairs[qu.number]
                    cho = ch[chno-1]
                    if an:
                        an.delete()
                    an = SingleChoiceAnswer(user=request.user, question=qu, choice=cho)
                    an.save
                    trip[2] = an

            context["triplets"] = triplets
            form = SubmissionForm( initial={'user': request.user, 'assignment':test.pk} )
            context['form'] = form

            if 'submit-test' in request.POST:
                # update submission
                submission = form.save(commit=False)
                submission.save()
                # we need to update the answers too
                for answer in form.cleaned_data['answers']:
                    if answer:
                        answer.submission = submission
                        answer.save()
            return render(request,'homework/sctest.html', context)

        else:
            context['debug'] = form.errors
            return render(request,'core/index.html', context)
    else: # not POST
        return render(request,'homework/sctest.html', context)
