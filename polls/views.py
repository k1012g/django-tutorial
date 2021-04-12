from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Choice, Question

# Create your views here.
def index(req):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {'latest_question_list' : latest_question_list}
    return render(req, 'polls/index.html', context)

def detail(req, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(req, 'polls/detail.html', {'question' : question})

def vote(req, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(req, 'polls/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', question_id)

def results(req, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(req, 'polls/results.html', {'question' : question})
