# Generated by Django 2.2.5 on 2019-10-08 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0002_auto_20191008_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='motionpicture',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
    ]