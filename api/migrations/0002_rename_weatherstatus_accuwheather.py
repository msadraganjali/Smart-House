# Generated by Django 4.2.5 on 2024-03-03 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='weatherStatus',
            new_name='AccuWheather',
        ),
    ]
