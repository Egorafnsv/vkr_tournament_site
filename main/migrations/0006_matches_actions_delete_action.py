# Generated by Django 4.0.4 on 2022-05-12 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_action_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='matches',
            name='actions',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.DeleteModel(
            name='Action',
        ),
    ]