# Generated by Django 4.1.5 on 2023-10-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0002_alter_link_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='token',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]