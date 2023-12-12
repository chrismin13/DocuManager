from django.contrib import admin
from .models import Company, Document

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'year']
    search_fields = ['title', 'company__name']
    list_filter = ['company', 'year']
