# Generated by Django 2.2.5 on 2019-11-04 05:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_date_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MotionPicture',
            fields=[
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_date_time', models.DateTimeField(auto_now=True)),
                ('mp_type', models.CharField(default='Movie', max_length=15)),
                ('name', models.CharField(db_index=True, max_length=140)),
                ('genre', models.CharField(max_length=15)),
                ('release_date', models.DateField(default=datetime.date(2019, 11, 4))),
                ('description', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3)),
                ('movie_id', models.SlugField(primary_key=True, serialize=False, unique=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_date_time', models.DateTimeField(auto_now=True)),
                ('review', models.TextField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movieapp.MotionPicture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_date_time', models.DateTimeField(auto_now=True)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movieapp.MotionPicture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_date_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=40)),
                ('movies', models.ManyToManyField(to='movieapp.MotionPicture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_date_time', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movieapp.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_date_time', models.DateTimeField(auto_now=True)),
                ('artist_type', models.CharField(default='Actor', max_length=15)),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('birthday', models.DateField(default=None)),
                ('description', models.TextField(default='')),
                ('image', models.ImageField(upload_to='images/')),
                ('approved', models.BooleanField(default=False)),
                ('artist_id', models.SlugField(primary_key=True, serialize=False, unique=True)),
                ('movies', models.ManyToManyField(to='movieapp.MotionPicture')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
