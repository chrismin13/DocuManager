from django.db import models
from django.conf import settings
from django.utils.text import slugify
import os
from datetime import datetime
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    slug = models.SlugField(unique=True, editable=False)  # Make slug not editable
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        # Generate slug from the company name if it doesn't already exist
        if not self.id:
            self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

def document_upload_to(instance, filename):
    # Create a unique file name using timestamp
    base, extension = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_file_name = f"{base}_{timestamp}{extension}"

    # Create a clean company name slug for folder name
    company_slug = slugify(instance.company.name)
    return os.path.join('documents', company_slug, unique_file_name)

class Document(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField()
    document = models.FileField(upload_to=document_upload_to)
    slug = models.SlugField(unique=True, editable=False)  # Make slug not editable

    def save(self, *args, **kwargs):
        # Generate slug from the document title if it doesn't already exist
        if not self.id:
            self.slug = slugify(self.title)
        super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Rating(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('company', 'user')

    def __str__(self):
        return f"{self.score} by {self.user.username} for {self.company.name}"
    
class DocumentView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'document')

    def __str__(self):
        return f"{self.document.title} viewed by {self.user.username}"
