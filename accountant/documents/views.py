from django.shortcuts import redirect, render, get_object_or_404
from .models import Company, Document
from django.contrib.auth.decorators import login_required
from .forms import CompanyForm
from django.db.models import Q

def company_list(request):
    companies = Company.objects.all()
    return render(request, 'documents/company_list.html', {'companies': companies})

def company_detail(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    documents_by_year = Document.objects.filter(company=company).order_by('-year')
    return render(request, 'documents/company_detail.html', {'company': company, 'documents': documents_by_year})

def document_detail(request, company_slug, year, document_title):
    document = get_object_or_404(Document, company__slug=company_slug, year=year, title=document_title)
    return render(request, 'documents/document_detail.html', {'document': document})

def search_results(request):
    query = request.GET.get('query', '')
    documents = Document.objects.filter(
        Q(title__icontains=query) | 
        Q(company__name__icontains=query) | 
        Q(year__icontains=query)
    )
    return render(request, 'documents/search_results.html', {'documents': documents})

@login_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            return redirect('some_view')  # Redirect to a relevant page
    else:
        form = CompanyForm()
    return render(request, 'documents/add_company.html', {'form': form})