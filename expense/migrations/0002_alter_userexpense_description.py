# Generated by Django 3.2 on 2021-05-07 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexpense',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
