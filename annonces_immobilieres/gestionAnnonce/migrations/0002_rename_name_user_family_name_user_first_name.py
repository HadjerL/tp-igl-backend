# Generated by Django 4.1.4 on 2022-12-27 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAnnonce', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='family_name',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]