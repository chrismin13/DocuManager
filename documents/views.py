from django.shortcuts import redirect, render, get_object_or_404
from .models import Company, Document, Rating, DocumentView
from django.contrib.auth.decorators import login_required
from .forms import CompanyForm, SignUpForm, UserEditForm, DocumentForm, RatingForm
from django.db.models import Q, Avg, F
from django.contrib.auth import authenticate, login, logout

def company_list(request):
    companies = Company.objects.all()
    most_viewed_documents = None
    if request.user.is_authenticated:
        most_viewed_documents = DocumentView.objects.filter(user=request.user).order_by('-views')[:5]
    return render(request, 'documents/company_list.html', {
        'companies': companies,
        'most_viewed_documents': most_viewed_documents
    })


def company_detail(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    documents_by_year = Document.objects.filter(company=company).order_by('-year')
    average_rating = company.ratings.aggregate(average_score=Avg('score'))['average_score']
    rating_count = company.ratings.count()
    
    # Check if the user has already rated the company
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(company=company, user=request.user).first()

    # Keep average rating up to 2 decimal places
    if average_rating:
        average_rating = round(average_rating, 2)
    return render(request, 'documents/company_detail.html', {
        'company': company, 
        'documents': documents_by_year, 
        'average_rating': average_rating,
        'rating_count': rating_count,
        'user_rating': user_rating
    })


def document_detail(request, company_slug, year, document_title):
    document = get_object_or_404(Document, company__slug=company_slug, year=year, title=document_title)
    if request.user.is_authenticated:
        DocumentView.objects.get_or_create(user=request.user, document=document)
        DocumentView.objects.filter(user=request.user, document=document).update(views=F('views') + 1)
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
            return redirect('/' + company.slug)  # Redirect to a relevant page
    else:
        form = CompanyForm()
    return render(request, 'documents/add_company.html', {'form': form})

@login_required
def edit_company(request, company_slug):
    if request.user.is_superuser:
        company = get_object_or_404(Company, slug=company_slug)
    else:
        company = get_object_or_404(Company, slug=company_slug, owner=request.user)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            return redirect('company_detail', company_slug=company.slug)
    else:
        form = CompanyForm(instance=company)
    return render(request, 'documents/edit_company.html', {'form': form})

@login_required
def delete_company(request, company_slug):
    if request.user.is_superuser:
        company = get_object_or_404(Company, slug=company_slug)
    else:
        company = get_object_or_404(Company, slug=company_slug, owner=request.user)
    if request.method == 'POST':
        company.delete()
        return redirect('company_list')
    return render(request, 'documents/confirm_delete.html', {'company': company})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in after sign up
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('signup_success')  # Redirect to a home or profile page
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def signup_success(request):
    return render(request, 'registration/signup_success.html')

def custom_logout(request):
    logout(request)
    return render(request, 'registration/logout_success.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the profile page
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

@login_required
def add_document(request, company_slug):
    if request.user.is_superuser:
        company = get_object_or_404(Company, slug=company_slug)
    else:
        company = get_object_or_404(Company, slug=company_slug, owner=request.user)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.company = company
            document.save()
            return redirect('company_detail', company_slug=company.slug)
    else:
        form = DocumentForm()
    return render(request, 'documents/add_document.html', {'form': form, 'company': company})

@login_required
def edit_document(request, company_slug, document_id):
    if request.user.is_superuser:
        company = get_object_or_404(Company, slug=company_slug)
    else:
        company = get_object_or_404(Company, slug=company_slug, owner=request.user)
    document = get_object_or_404(Document, id=document_id, company=company)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('company_detail', company_slug=company.slug)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/edit_document.html', {'form': form, 'company': company})


@login_required
def delete_document(request, company_slug, document_id):
    if request.user.is_superuser:
        company = get_object_or_404(Company, slug=company_slug, owner=request.user)
    else:
        company = get_object_or_404(Company, slug=company_slug, owner=request.user)
    document = get_object_or_404(Document, id=document_id, company=company)
    if request.method == 'POST':
        document.delete()
        return redirect('company_detail', company_slug=company.slug)
    return render(request, 'documents/confirm_delete_document.html', {'document': document, 'company': company})

@login_required
def submit_rating(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                company=company,
                user=request.user,
                defaults={'score': form.cleaned_data['score']}
            )
            if not created:
                rating.score = form.cleaned_data['score']
                rating.save()
            return redirect('company_detail', company_slug=company_slug)
    else:
        form = RatingForm()
    return render(request, 'documents/rate_company.html', {'form': form, 'company': company})

