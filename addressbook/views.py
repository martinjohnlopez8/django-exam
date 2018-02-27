from django.shortcuts import render
from django.shortcuts import get_object_or_404
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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from braces import views

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
	form_class = ContactForm
	context_object_name = 'contacts'

	def get_queryset(self):
		queryset = Contact.objects.filter(user=self.request.user)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ContactListView, self).get_context_data(**kwargs)
		user = self.request.user
		contact_create_form = ContactForm()
		context.update({
			'form': contact_create_form
		})
		return context

class ContactUpdateView(UpdateView):
	model = Contact
	template_name = 'addressbook/edit_contact.html'
	form_class = ContactForm
	success_url = reverse_lazy('addressbook:home')

	pk_url_kwarg = 'contact_id'

	def post(self, request, *args, **kwargs):
		form = ContactForm(self.request.POST)
		print(self.request.POST)
		if form.is_valid():
			print("TAMA")
		else:
			print('MALI')
		return redirect('addressbook:home')

	def get_object(self):
		contact_id = self.kwargs.get('contact_id', None)
		print(contact_id)
		return get_object_or_404(Contact, pk=contact_id )

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

class AjaxContactCreateView(views.JSONResponseMixin, views.AjaxResponseMixin, View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super(AjaxContactCreateView, self).dispatch(request, *args, **kwargs)

	def post_ajax(self, request, *args, **kwargs):
		user = self.request.user
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		contact_number = request.POST.get('contact_number')
		address = request.POST.get('address')

		data = {}
		data['first_name'] = first_name
		data['last_name'] = last_name
		data['contact_number'] = contact_number
		data['address'] = address

		contact = Contact()
		contact.user = user
		contact.first_name = first_name
		contact.last_name = last_name
		contact.contact_number = contact_number
		contact.address = address
		contact.save()

		print(data)
		return self.render_json_response(data)

class AjaxContactUpdateView(views.JSONResponseMixin, views.AjaxResponseMixin, View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super(AjaxContactUpdateView, self).dispatch(request, *args, **kwargs)

	def post_ajax(self, request, *args, **kwargs):
		user = self.request.user
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		contact_number = request.POST.get('contact_number')
		address = request.POST.get('address')

		data = {}
		data['first_name'] = first_name
		data['last_name'] = last_name
		data['contact_number'] = contact_number
		data['address'] = address

		contact = Contact()
		contact.user = user
		contact.first_name = first_name
		contact.last_name = last_name
		contact.contact_number = contact_number
		contact.address = address
		contact.save()

		print(data)
		return self.render_json_response(data)

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