# Generated by Django 4.2 on 2024-04-11 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0006_remove_tblivro_tombo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblivro',
            name='tombo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
