# Generated by Django 3.1.2 on 2020-10-07 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnae_registration',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]