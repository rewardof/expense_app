# Generated by Django 3.2 on 2021-06-20 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_auto_20210507_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userexpense',
            options={'ordering': ['-date_added'], 'permissions': (('can_view_expenses', 'Grandfather or father can view all family members expenses'),)},
        ),
    ]