# Generated by Django 4.2.5 on 2024-03-16 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_guiorderclassmodel_home'),
    ]

    operations = [
        migrations.AddField(
            model_name='grafdata',
            name='temp2',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]