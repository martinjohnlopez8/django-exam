from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Contact(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	contact_number = PhoneNumberField(default="+639171231234")
	address = models.CharField(max_length=255)

	def __str__(self):
		return self.first_name + " " + self.last_name
