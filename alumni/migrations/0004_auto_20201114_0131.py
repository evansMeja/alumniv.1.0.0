# Generated by Django 3.1.2 on 2020-11-13 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni', '0003_auto_20201007_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='picture',
            field=models.FileField(blank=True, default='default/anony.jpg', null=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='story',
            name='picture_present',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='story',
            name='video_present',
            field=models.BooleanField(default=False),
        ),
    ]
