# Generated by Django 3.2.6 on 2021-08-24 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210814_2143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['created_at']},
        ),
    ]
