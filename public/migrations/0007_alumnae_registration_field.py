# Generated by Django 3.1.2 on 2020-10-09 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0006_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnae_registration',
            name='field',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='public.field'),
        ),
    ]
