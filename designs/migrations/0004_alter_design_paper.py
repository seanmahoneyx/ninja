# Generated by Django 5.2.1 on 2025-05-22 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0003_design_status_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='paper',
            field=models.CharField(max_length=50),
        ),
    ]
