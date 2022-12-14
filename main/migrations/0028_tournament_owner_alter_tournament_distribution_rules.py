# Generated by Django 4.0.4 on 2022-05-22 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0027_tournament_distribution_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='tournaments', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='distribution_rules',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
