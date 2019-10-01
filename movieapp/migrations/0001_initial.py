# Generated by Django 2.2.5 on 2019-10-01 08:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MotionPicture',
            fields=[
                ('movie_id', models.AutoField(primary_key=True, serialize=False)),
                ('mp_type', models.CharField(default='Movie', max_length=15)),
                ('name', models.CharField(max_length=140)),
                ('genre', models.CharField(max_length=15)),
                ('release_date', models.DateField()),
                ('description', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movieapp.MotionPicture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('artist_id', models.AutoField(primary_key=True, serialize=False)),
                ('artist_type', models.CharField(default='Actor', max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default='')),
                ('image', models.ImageField(upload_to='')),
                ('movies', models.ManyToManyField(to='movieapp.MotionPicture')),
            ],
        ),
    ]
