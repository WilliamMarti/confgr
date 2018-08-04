from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):

	username = 'wmarti'

	context = {'username': username}

	return render(request, 'core/home.html', context)
