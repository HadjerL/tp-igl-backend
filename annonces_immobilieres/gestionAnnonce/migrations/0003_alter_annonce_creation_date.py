# Generated by Django 4.1.4 on 2022-12-29 23:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAnnonce', '0002_annonce_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annonce',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
