from django.urls import path
from . import views

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('search/', views.search_results, name='search_results'),
    path('<slug:company_slug>/', views.company_detail, name='company_detail'),
    path('<slug:company_slug>/<int:year>/<slug:document_title>/', views.document_detail, name='document_detail'),
    path('add_company/', views.add_company, name='add_company'),
]
