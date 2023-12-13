from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('search/', views.search_results, name='search_results'),
    # User management
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', next_page='company_list'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/success/', views.signup_success, name='signup_success'),
    path('profile/', views.profile, name='profile'),
    # Company management from users
    path('add_company/', views.add_company, name='add_company'),
    path('edit_company/<slug:company_slug>/', views.edit_company, name='edit_company'),
    path('delete_company/<slug:company_slug>/', views.delete_company, name='delete_company'),
    # Document management from users
    path('company/<slug:company_slug>/add_document/', views.add_document, name='add_document'),
    path('company/<slug:company_slug>/rate/', views.submit_rating, name='submit_rating'),
    path('company/<slug:company_slug>/edit_document/<int:document_id>/', views.edit_document, name='edit_document'),
    path('company/<slug:company_slug>/delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
    # The following paths must be at the bottom of the list because they are more general than the ones above
    path('<slug:company_slug>/', views.company_detail, name='company_detail'),
    path('<slug:company_slug>/<int:year>/<slug:document_slug>/', views.document_detail, name='document_detail'),
]
