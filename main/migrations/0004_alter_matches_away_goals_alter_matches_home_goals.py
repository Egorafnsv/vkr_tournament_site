# Generated by Django 4.0.4 on 2022-05-10 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_tournament_type_delete_typetournament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matches',
            name='away_goals',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='matches',
            name='home_goals',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
