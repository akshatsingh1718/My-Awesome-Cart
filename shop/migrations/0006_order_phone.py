# Generated by Django 3.0.5 on 2020-05-08 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200508_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.IntegerField(default=0),
        ),
    ]
