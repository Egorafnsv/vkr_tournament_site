# Generated by Django 4.0.4 on 2022-05-14 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_playoff_scheme_club_away_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='actions',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
