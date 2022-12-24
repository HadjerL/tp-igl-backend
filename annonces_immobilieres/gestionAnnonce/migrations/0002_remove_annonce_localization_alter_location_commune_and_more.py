# Generated by Django 4.1.4 on 2022-12-24 12:27

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAnnonce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annonce',
            name='localization',
        ),
        migrations.AlterField(
            model_name='location',
            name='commune',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='wilaya', chained_model_field='Wilaya', default='', on_delete=django.db.models.deletion.CASCADE, related_name='location', to='gestionAnnonce.commune'),
        ),
        migrations.AlterField(
            model_name='location',
            name='wilaya',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='location', to='gestionAnnonce.wilaya'),
        ),
    ]
