# Generated by Django 5.2.1 on 2025-05-22 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designs', '0004_alter_design_paper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='design',
            name='design_num',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
