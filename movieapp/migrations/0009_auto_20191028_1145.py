# Generated by Django 2.2.5 on 2019-10-28 11:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0008_category_categorylabel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='approved',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='artist',
            name='artist_id',
            field=models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(db_index=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='motionpicture',
            name='approved',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='motionpicture',
            name='movie_id',
            field=models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='motionpicture',
            name='name',
            field=models.CharField(db_index=True, max_length=140),
        ),
        migrations.AlterField(
            model_name='motionpicture',
            name='release_date',
            field=models.DateField(default=datetime.date(2019, 10, 28)),
        ),
    ]