# Generated by Django 4.0.4 on 2022-05-13 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_matches_actions_delete_action'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tables',
            old_name='test',
            new_name='points',
        ),
    ]
