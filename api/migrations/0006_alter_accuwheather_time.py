# Generated by Django 4.2.5 on 2024-03-03 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_date_accuwheather_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accuwheather',
            name='time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
