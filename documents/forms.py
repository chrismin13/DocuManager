from django import forms
from .models import Company, Document, Rating
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'logo']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('A user with that email already exists.')
        return email
    
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'year', 'document']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(choices=[(i, i) for i in range(1, 6)])
        }

class DocumentFilterForm(forms.Form):
    year = forms.ChoiceField(choices=[])  # Initially empty, will be set in the view