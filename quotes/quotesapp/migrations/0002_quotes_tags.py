# Generated by Django 4.1.5 on 2023-01-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotesapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='tags',
            field=models.ManyToManyField(to='quotesapp.tags'),
        ),
    ]
