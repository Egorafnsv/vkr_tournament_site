# Generated by Django 4.0.4 on 2022-05-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_matches_text_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playoff_scheme',
            name='away_goals',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playoff_scheme',
            name='home_goals',
            field=models.PositiveIntegerField(default=0),
        ),
    ]