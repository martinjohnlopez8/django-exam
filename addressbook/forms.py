from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from .models import Contact

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ('first_name', 'last_name', 'contact_number', 'address')

