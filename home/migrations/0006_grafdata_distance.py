# Generated by Django 4.2.5 on 2024-04-21 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_guiorderclassmodel_blue_guiorderclassmodel_green_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grafdata',
            name='distance',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
