# Generated by Django 4.0.4 on 2022-05-17 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_tournament_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tables',
            name='goals_difference',
            field=models.IntegerField(default=0),
        ),
    ]
