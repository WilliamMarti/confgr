from django.db import models

class Device(models.Model):

	# Router1
	name = models.CharField(max_length=30)

	# router/switch/AP
	device_type = models.CharField(max_length=30)

	# ISR4331/CAT2960
	model = models.CharField(max_length=30)

	# New York/San Diego
	site = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class User(models.Model):

	username = models.CharField(max_length=30)

	firstname = models.CharField(max_length=30)

	lastname = models.CharField(max_length=30)

	email = models.CharField(max_length=30)

	def __str__(self):
		return self.username