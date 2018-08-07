from django.shortcuts import render
from django.http import HttpResponse



from core.models import Device
from django.contrib.auth.models import User

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

def profile(request, searchedusername):

	searchedusername = User.objects.filter(username=searchedusername)

	page = searchedusername[0].username
	title = "Confgr - " + str(page)

	devices = Device.objects.all()

	context = {'username': searchedusername[0].username,
				'searchedusername': searchedusername[0].username,
				'title': title,
				'devices': devices,
				'firstname': searchedusername[0].first_name,
				'lastname': searchedusername[0].last_name,
				'email': searchedusername[0].email,}

	return render(request, 'core/profile.html', context)



def profileedit(request, searchedusername):

	searchedusername = User.objects.filter(username=searchedusername)

	page = searchedusername[0].username
	title = "Confgr - " + str(page)

	devices = Device.objects.all()

	context = {'username': searchedusername[0].username,
				'searchedusername': searchedusername[0].username,
				'title': title,
				'devices': devices,
				'firstname': searchedusername[0].first_name,
				'lastname': searchedusername[0].last_name,
				'email': searchedusername[0].email,}

	return render(request, 'core/profileedit.html', context)
