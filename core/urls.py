from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('inventory', views.inventory, name='inventory'),
	path('user/<searchedusername>', views.profile, name='profile'),
	path('user/<searchedusername>/edit', views.profileedit, name='profileedit'),
]