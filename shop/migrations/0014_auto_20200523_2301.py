# Generated by Django 3.0.5 on 2020-05-23 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_loginperson'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loginperson',
            old_name='address',
            new_name='address1',
        ),
    ]
