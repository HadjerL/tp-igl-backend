<<<<<<< HEAD
# Generated by Django 4.1.4 on 2022-12-31 12:35

import datetime
=======
# Generated by Django 4.1.4 on 2022-12-31 20:02

import datetime
from django.conf import settings
>>>>>>> d970fd54904ac465278dc70296a88ef1e442e794
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
=======
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('family_name', models.CharField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=254, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
>>>>>>> d970fd54904ac465278dc70296a88ef1e442e794
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(default='', max_length=50)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
<<<<<<< HEAD
            name='Annonce',
=======
            name='Annoncement',
>>>>>>> d970fd54904ac465278dc70296a88ef1e442e794
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=35)),
                ('interface', models.FloatField(default=0.0)),
                ('prix', models.FloatField(default=0.0)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Caregorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_cat', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=35)),
                ('prenom', models.CharField(max_length=35)),
                ('adresse', models.CharField(max_length=50)),
                ('tele', phone_field.models.PhoneField(max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Wilaya',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=35, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='gestionAnnonce.address')),
                ('commune', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='wilaya', chained_model_field='wilaya', default=None, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='gestionAnnonce.commune')),
                ('wilaya', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='gestionAnnonce.wilaya')),
            ],
        ),
        migrations.AddField(
            model_name='commune',
            name='wilaya',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='commune', to='gestionAnnonce.wilaya'),
        ),
        migrations.CreateModel(
            name='AnnoncementImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='photo%y%m%d')),
<<<<<<< HEAD
                ('annoncement', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gestionAnnonce.annonce')),
            ],
        ),
        migrations.AddField(
            model_name='annonce',
=======
                ('annoncement', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gestionAnnonce.annoncement')),
            ],
        ),
        migrations.AddField(
            model_name='annoncement',
>>>>>>> d970fd54904ac465278dc70296a88ef1e442e794
            name='caregorie',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='annonce', to='gestionAnnonce.caregorie'),
        ),
        migrations.AddField(
<<<<<<< HEAD
            model_name='annonce',
=======
            model_name='annoncement',
>>>>>>> d970fd54904ac465278dc70296a88ef1e442e794
            name='contact',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='annonce', to='gestionAnnonce.contact'),
        ),
        migrations.AddField(
<<<<<<< HEAD
            model_name='annonce',
=======
            model_name='annoncement',
>>>>>>> d970fd54904ac465278dc70296a88ef1e442e794
            name='location',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='annonce', to='gestionAnnonce.location'),
        ),
        migrations.AddField(
<<<<<<< HEAD
            model_name='annonce',
            name='type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='annonce', to='gestionAnnonce.type'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(default='', max_length=254, unique=True)),
                ('family_name', models.CharField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=254, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
=======
            model_name='annoncement',
            name='type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='annonce', to='gestionAnnonce.type'),
        ),
        migrations.AddField(
            model_name='annoncement',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='annonce', to=settings.AUTH_USER_MODEL),
>>>>>>> d970fd54904ac465278dc70296a88ef1e442e794
        ),
    ]
