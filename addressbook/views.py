from django.shortcuts import render
from django.contrib.auth import login as user_login, authenticate
from django.contrib.auth import logout as user_logout
from django.shortcuts import redirect
from tablib import Dataset
from .forms import ContactForm
from django.contrib.auth.forms import UserCreationForm
from tablib import Dataset
from .resources import ContactResource
from django.http import HttpResponse

from .models import Contact

# Create your views here.

def home(request):
	if request.POST.get('login'):
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        user_login(request, user)
	        return redirect('addressbook:home')
	    else:
	        print('Error logging in')
	elif request.POST.get('signup'):
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			user_login(request, user)
			return redirect('addressbook:home')
	form = UserCreationForm()
	if request.user.is_authenticated:
		contacts = Contact.objects.filter(user=request.user)
		return render(request, 'addressbook/home.html', {
			'contacts': contacts
		})
	return render(request, 'addressbook/login.html', {
		'form': form,
	})

def add_contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			contact = form.save(commit=False)
			contact.user = request.user
			contact.save()
			return redirect('addressbook:home')
	else:
		form = ContactForm()
	return render(request, 'addressbook/add_contact.html', {
		'form': form
	})

def edit_contact(request, contact_id):
	contact = Contact.objects.get(id=contact_id)
	if request.method == "POST":
		form = ContactForm(request.POST, instance=contact)
		if form.is_valid():
			contact.save()
			return redirect('addressbook:home')
	else:
		form = ContactForm(instance=contact)
	return render(request, 'addressbook/edit_contact.html', {
		'form': form
	})

def contact(request, contact_id):
	member = Member.objects.get(id=musician_id)
	if request.method == "POST":
		form = MemberForm(request.POST, instance=member)
		if form.is_valid():
			member.save()
			return redirect('band:musician_list')
	else:
		form = MemberForm(instance=member)
	return render(request, 'band/edit_musician.html', {
		'form': form
	})

def delete_contact(request, contact_id):
	contact = Contact.objects.get(id=contact_id)
	contact.delete()
	return redirect('addressbook:home')

def delete_confirmation(request, contact_id):
	contact = Contact.objects.get(id=contact_id)
	return render(request, 'addressbook/delete_confirmation.html', {
		'contact': contact
	})

def export_csv(request):
	queryset = Contact.objects.filter(user=request.user)
	contact_resource = ContactResource()
	dataset = contact_resource.export(queryset)
	response = HttpResponse(dataset.csv, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
	return response

def import_csv(request):
	if request.method == 'POST':
		contacts_resource = ContactResource()
		dataset = Dataset()
		new_contacts = request.FILES['import-csv']

		try:
			imported_data = dataset.load(new_contacts.read().decode('utf-8'),format='csv')
			result = contacts_resource.import_data(dataset, dry_run=True)
			print('success')
			return redirect('addressbook:home')

		except:
			contacts_resource.import_data(dataset, dry_run=False)
			error = 'Error importing CSV file'
			return render(request, 'addressbook/import.html', {'error': error})

	return render(request, 'addressbook/import.html', {})


def logout(request):
	user_logout(request)
	return redirect('addressbook:home')


