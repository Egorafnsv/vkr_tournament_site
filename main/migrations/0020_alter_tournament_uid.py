# Generated by Django 4.0.4 on 2022-05-17 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_tournament_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='uid',
            field=models.CharField(default='trnmt-tmp', max_length=20),
        ),
    ]
