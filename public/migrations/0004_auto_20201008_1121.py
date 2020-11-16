# Generated by Django 3.1.2 on 2020-10-08 08:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('public', '0003_alumnae_registration_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumnae_registration',
            name='followers',
            field=models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
