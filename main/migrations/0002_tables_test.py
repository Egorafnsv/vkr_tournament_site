# Generated by Django 4.0.4 on 2022-05-08 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tables',
            name='test',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
