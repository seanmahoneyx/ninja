# Generated by Django 5.2.1 on 2025-05-22 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='active_status',
            new_name='is_active',
        ),
    ]
