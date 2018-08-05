from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):

	username = 'wmarti'
	page = "Home"
	title = "Confgr - " + page

	context = {'username': username,
				'title': title}

	return render(request, 'core/home.html', context)
