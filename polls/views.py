import random
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q 

from .models import Question,Choice
# Create your views here.
latest_question_list= Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
question_list= Question.objects.filter(pub_date__lte=timezone.now()).all()
random_question = random.choice(question_list)

def index(request):
    return render(request, "polls/index.html",{
        "latest_question_list": latest_question_list,
        "random_question":random_question,
    })

def allpolls(request):
    if request.method =='POST':
        question = request.POST['question']
        if question:
            author = request.POST['author']
            option1 = request.POST['option1']
            option2 = request.POST['option2']
            option3 = request.POST['option3']
            option4 = request.POST['option4']
            if not Question.objects.filter(question_text =question):
                question=Question.objects.create(question_text= question,author=author,pub_date=timezone.now())
                if option1:
                    Choice.objects.create(question=question,choice_text=option1)
                if option2:
                    Choice.objects.create(question=question,choice_text=option2)
                if option3:
                    Choice.objects.create(question=question,choice_text=option3)
                if option4:
                    Choice.objects.create(question=question,choice_text=option4)
                return render(request, "polls/allpolls.html",{
                    'message':"Question added successfully.",
                    'question_list':question_list,
                    "random_question":random_question,
                })
            else:
                return render(request, "polls/allpolls.html",{
                    'message':"Question already exists!",
                    'question_list':question_list,
                    "random_question":random_question,
                })

    
    return render(request, "polls/allpolls.html",{
    'question_list':question_list,
    "random_question":random_question,
    })
    

            

def detail(request,question_id):
    question= Question.objects.get( pk=question_id)
    if question.pub_date <= timezone.now():

        return render(request,'polls/detail.html',{
            "question":question,
            "random_question":random_question,
        })
    else:
         return render(request,'polls/detail.html',{
            'message':"Not published yet!",
            "random_question":random_question,
        })


def result(request,question_id):
    question= Question.objects.get(pk=question_id)
    return render(request, "polls/result.html",{
        "question": question,
        "random_question":random_question,
    })


def vote(request,question_id):
    if request.method =="POST":
        question= Question.objects.get(pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk = request.POST['choice'])
        except: 
            return render(request,'polls/detail.html',{
                "question": question,
                "message": "Please select an option.",
                "random_question":random_question,
            })
        else:
            selected_choice.vote +=1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:result',args=(question_id,)))

def search(request):
    query = request.GET.get('q','')
    if query:
        qset = (
            Q(question_text__icontains= query)
            )
        results = Question.objects.filter(qset).distinct()
    
        if results:
            return render(request, 'polls/search.html',{
                'results': results,
                'query':query,
                "random_question":random_question,

            })
        else:
            return render(request, 'polls/search.html',{
                "message":"No result found.",
                'query':query,
                "random_question":random_question,
            })
            

    else: 
        return render(request, "polls/search.html",{
                'message':"Please write a query.",
                "random_question":random_question,
            })