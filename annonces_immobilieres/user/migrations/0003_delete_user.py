# Generated by Django 4.1.4 on 2022-12-22 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_annonce_alter_user_nom_alter_user_prenom'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
