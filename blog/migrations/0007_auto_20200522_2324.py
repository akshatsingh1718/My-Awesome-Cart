# Generated by Django 3.0.5 on 2020-05-22 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_remove_blogpost_heading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=models.TextField(default='', max_length=30000),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
    ]
