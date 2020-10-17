from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    context = {'name' : "Rowen"}
    return render(request, 'viewgraph/index.html', context)

# Create your views here.
