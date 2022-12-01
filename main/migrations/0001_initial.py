# Generated by Django 4.0.4 on 2022-05-08 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clubs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TypeTournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('L', 'league'), ('P', 'playoffs'), ('LP', 'league + playoffs')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.typetournament')),
            ],
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('win', models.PositiveIntegerField(default=0)),
                ('draw', models.PositiveIntegerField(default=0)),
                ('lose', models.PositiveIntegerField(default=0)),
                ('goals_for', models.PositiveIntegerField(default=0)),
                ('goals_against', models.PositiveIntegerField(default=0)),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.clubs')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=50)),
                ('goals', models.PositiveIntegerField(default=0)),
                ('yellow', models.PositiveIntegerField(default=0)),
                ('red', models.PositiveIntegerField(default=0)),
                ('disqualified', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.clubs')),
            ],
        ),
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_goals', models.PositiveIntegerField(default=0)),
                ('away_goals', models.PositiveIntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('stage', models.PositiveIntegerField()),
                ('club_away', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='club_away', to='main.clubs')),
                ('club_home', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='club_home', to='main.clubs')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
        migrations.AddField(
            model_name='clubs',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament'),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.clubs')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.matches')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.players')),
            ],
        ),
    ]
