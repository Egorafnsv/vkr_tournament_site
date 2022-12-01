# Generated by Django 4.0.4 on 2022-05-30 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0035_tournament_admins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tournament', to=settings.AUTH_USER_MODEL),
        ),
    ]
