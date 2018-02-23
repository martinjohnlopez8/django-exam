from django.shortcuts import render
from django.contrib.auth import login as user_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout as user_logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from tablib import Dataset
from .forms import ContactForm
from django.contrib.auth.forms import UserCreationForm
from tablib import Dataset
from .resources import ContactResource
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import FormView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from .models import Contact

# Create your views here.

class LoginView(FormView):
	template_name = 'addressbook/login.html'
	form_class = UserCreationForm

	def post(self, request, *args, **kwargs):
		if 'login' in request.POST:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				user_login(request, user)
				return redirect('addressbook:home')
			else:
				return redirect('addressbook:login')


		elif 'signup' in request.POST:
			form = UserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				username = form.cleaned_data.get('username')
				raw_password = form.cleaned_data.get('password1')
				user = authenticate(username=username, password=raw_password)
				user_login(request, user)
				return redirect('addressbook:home')

class ContactListView(ListView):
	model = Contact
	template_name = 'addressbook/home.html'
	context_object_name = 'contacts'

	def get_queryset(self):
		queryset = Contact.objects.filter(user=self.request.user)
		return queryset


class ContactCreateView(CreateView):
	template_name = 'addressbook/add_contact.html'
	form_class = ContactForm

	def get_query(self):
		return Contact.objects.filter(user=self.request.user)

	def form_valid(self, form):
		contact = form.save(commit=False)
		contact.user = self.request.user
		contact.save()
		return redirect('addressbook:home')

class ContactUpdateView(UpdateView):
	model = Contact
	template_name = 'addressbook/edit_contact.html'
	form_class = ContactForm
	success_url = reverse_lazy('addressbook:home')

	pk_url_kwarg = 'contact_id'

	def get_query(self):
		return Contact.objects.filter(user=self.request.user)

class ContactDeleteView(DeleteView):
	model = Contact
	success_url = reverse_lazy('addressbook:home')

	pk_url_kwarg = 'contact_id'

class LogoutView(View):
	def get(self, request):
		user_logout(request)
		return redirect('addressbook:login')

def export_csv(request):
	queryset = Contact.objects.defer('id', 'user').filter(user=request.user)
	contact_resource = ContactResource()
	dataset = contact_resource.export(queryset)
	response = HttpResponse(dataset.csv, content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="contacts.csv"'
	return response

def import_csv(request):
	if request.method == 'POST':
		contact = Contact.objects.filter(user=request.user)
		contacts_resource = ContactResource()
		dataset = Dataset()
		new_contacts = request.FILES['import-csv']

		try:
			imported_data = dataset.load(new_contacts.read().decode('utf-8'),format='csv')
			dataset.headers['user'] = request.user.id
			contacts_resource.import_data(dataset, dry_run=False)

		except:
			print(request.user.id)

	return render(request, 'addressbook/import.html', {})