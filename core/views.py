from django.shortcuts import render
from django.http import HttpResponse

from core.models import Device

# Create your views here.


def index(request):

	username = 'wmarti'
	page = "Home"
	title = "Confgr - " + page

	devices = Device.objects.all()

	context = {'username': username,
				'title': title,
				'devices': devices}

	return render(request, 'core/home.html', context)

def inventory(request):

	username = 'wmarti'
	page = "Inventory"
	title = "Confgr - " + page

	devices = Device.objects.all()

	context = {'username': username,
				'title': title,
				'devices': devices}

	return render(request, 'core/inventory.html', context)