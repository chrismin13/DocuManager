from django.db import models
from django.conf import settings
from django.utils.text import slugify
import os
from datetime import datetime

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

    def __str__(self):
        return self.title
