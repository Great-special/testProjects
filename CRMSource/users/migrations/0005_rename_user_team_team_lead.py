# Generated by Django 4.0.6 on 2022-08-16 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_teammember'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='user',
            new_name='team_lead',
        ),
    ]