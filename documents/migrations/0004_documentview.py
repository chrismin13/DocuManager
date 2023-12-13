# Generated by Django 4.2.7 on 2023-12-13 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0003_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=0)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.document')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'document')},
            },
        ),
    ]