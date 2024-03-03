# Generated by Django 4.2.5 on 2024-03-01 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='weatherStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.IntegerField()),
                ('status', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]