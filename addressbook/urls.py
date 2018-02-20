from django.urls import path

from . import views

app_name = 'addressbook'
urlpatterns = [
	path('', views.home, name='home'),
	path('logout/', views.logout, name='logout'),
	path('add/', views.add_contact, name='add_contact'),
	path('edit/<int:contact_id>', views.edit_contact, name='edit_contact'),
	path('delete/<int:contact_id>', views.delete_contact, name='delete_contact'),
	path('delete/confirmation/<int:contact_id>', views.delete_confirmation, name='delete_confirmation'),
	path('exportcsv', views.export_csv, name='export_csv'),
	path('importcsv', views.import_csv, name='import_csv')
]