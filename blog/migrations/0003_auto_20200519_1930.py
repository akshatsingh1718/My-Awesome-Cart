# Generated by Django 3.0.5 on 2020-05-19 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='author',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.CharField(default='', max_length=60),
        ),
    ]
