from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def greet(request):
    return HttpResponse("Hello!! welcome to django")
def info(request):
    data={
        'name':["sharanya","harish","chandu"],
        'age':[23,21,24],
        'city':['hyderabad','warangal','warangal']
    }
    return JsonResponse(data)

def calculator(request):
    a=int(request.GET.get('a',10))
    b=int(request.GET.get('b',2))
    results={
        "addition":a+b,
        "subtraction":a-b,
        "multiplication":a*b,
        "division":a/b
    }
    return JsonResponse(results)

