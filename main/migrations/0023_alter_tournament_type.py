# Generated by Django 4.0.4 on 2022-05-20 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_clubs_contact_info_matches_matchday_tournament_cards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='type',
            field=models.CharField(choices=[('L', 'tournament'), ('P', 'playoff')], max_length=2),
        ),
    ]