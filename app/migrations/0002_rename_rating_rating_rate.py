# Generated by Django 5.0.3 on 2024-03-17 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='rating',
            new_name='rate',
        ),
    ]