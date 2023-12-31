# Generated by Django 4.2.7 on 2023-12-12 15:54

from django.db import migrations, models
import django.db.models.deletion
import documents.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                ("logo", models.ImageField(blank=True, upload_to="company_logos/")),
                ("slug", models.SlugField(editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("year", models.IntegerField()),
                (
                    "document",
                    models.FileField(upload_to=documents.models.document_upload_to),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="documents.company",
                    ),
                ),
            ],
        ),
    ]
