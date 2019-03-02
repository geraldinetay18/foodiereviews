from django.http import HttpResponse, Http404, HttpResponseRedirect #no use if have render
from .models import *
from django.template import loader #no use it for #4
from django.shortcuts import render, get_object_or_404 #replace the 2 imported http above, this is #4
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def categories(request):
    return HttpResponse("You're looking at all the categories.")

def restaurants(request, category_id):
    return HttpResponse("You're looking at the restaurant list of category %s." % category_id)

'''
def details(request, restaurant_id):
    return HttpResponse("You're looking at the details of restaurant %s." % restaurant_id)
'''

#SAMPLE
@login_required
def add(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'reviewapp/add.html', {'restaurant': restaurant, 'user': request.user})

def test(request):
    if request.user.is_authenticated:
        return render(request, 'reviewapp/test.html', {'user': request.user})
    else:
        return render(request, 'reviewapp/test.html')

@login_required
def details(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'reviewapp/details.html', {'restaurant': restaurant, 'user': request.user})


#INDEX
'''
def index(request):
    # 1 return HttpResponse("Hello saphira")
    # 2
    latest_question_list = Question.objects.order_by('-pub_date')[:5]#order by date then return list of first 5 questions
    output= ','.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
    
    # 3
    template = loader.get_template('polls/index.html')
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context,request))

    # 4 - same as above #3 but use shortcut: render() --> removed template
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request,'polls/index.html',context)
'''
'''
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_question_list'
    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]
'''


#DETAIL
'''
def detail(request,question_id):
    # 1  return HttpResponse("You're looking at question %s." %question_id)
    # 3
    try:
        question= Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,'polls/detail.html',{'question':question})
    #4
    question = get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})
'''
'''
class DetailView(generic.DetailView):
    model=Question
    template_name='polls/detail.html'
'''

    
#RESULT
'''
def results(request,question_id):
    # 1
    response="You're looking at the results of question %s."
    return HttpResponse(response %question_id)

    #4
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/result.html',{'question':question})
'''
'''
class ResultView(generic.DetailView):
    model=Question
    template_name='polls/result.html'

'''

'''
def vote (request, question_id):
    # 1 return HttpResponse("You're voting on question %s." %question_id)
    # 3
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question' : question,
            'error_message' : "You didn't select a choice",
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
'''