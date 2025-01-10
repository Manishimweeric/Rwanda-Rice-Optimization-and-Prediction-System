# Generated by Django 4.1.13 on 2025-01-09 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, default='User', null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.role'),
        ),
    ]
