from django import forms
from phonenumber_field.modelfields import PhoneNumberField

from .models import Contact

class ContactForm(forms.ModelForm):
	address = forms.CharField(widget=forms.Textarea(
		attrs={
			'class': 'address'
		}))
	class Meta:
		model = Contact
		fields = ('first_name', 'last_name', 'contact_number', 'address')
		widgets = {
			'contact_number': forms.TextInput(attrs={'placeholder': 'eg: +639171231234'}),
			'address': forms.TextInput(attrs={'class': 'address'})
		}
