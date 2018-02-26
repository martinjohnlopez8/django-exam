from django.urls import path
from django.contrib.auth.decorators import login_required
from addressbook.views import ContactCreateView
from addressbook.views import ContactUpdateView
from addressbook.views import LoginView
from addressbook.views import ContactListView
from addressbook.views import ContactDeleteView
from addressbook.views import LogoutView
from addressbook.views import AjaxContactCreateView

from . import views

app_name = 'addressbook'
urlpatterns = [
	path('', login_required(ContactListView.as_view()), name='home'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('edit/<int:contact_id>', login_required(ContactUpdateView.as_view()), name='edit_contact'),
	path('delete/<int:contact_id>', login_required(ContactDeleteView.as_view()), name='delete_contact'),
	path('exportcsv/', views.export_csv, name='export_csv'),
	path('importcsv/', views.import_csv, name='import_csv'),
	path('login/', LoginView.as_view(), name='login'),
	path('testing/', AjaxContactCreateView.as_view(), name='testing')
]