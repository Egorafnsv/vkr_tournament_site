# Generated by Django 4.0.4 on 2022-05-23 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_matches_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='type',
            field=models.CharField(choices=[('L', 'league'), ('P', 'playoff')], max_length=2),
        ),
    ]