# Generated by Django 5.2.2 on 2025-06-08 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_remove_maintenance_cost_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maintenance',
            old_name='date',
            new_name='date_signing_contract',
        ),
        migrations.AddField(
            model_name='maintenance',
            name='date_expire_contract',
            field=models.DateField(default='2024-01-01'),
            preserve_default=False,
        ),
    ]
