# Generated by Django 4.0.4 on 2022-05-22 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_tournament_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='away_goals',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='matches',
            name='home_goals',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
