# Generated by Django 2.2.5 on 2019-10-09 02:05

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movieapp', '0003_motionpicture_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='birthday',
            field=models.DateField(default=datetime.date(2019, 10, 9)),
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('movies', models.ManyToManyField(to='movieapp.MotionPicture')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]