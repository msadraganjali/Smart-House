# Generated by Django 4.2.5 on 2024-03-13 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guiorderclassmodel',
            name='home',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.home'),
        ),
    ]
