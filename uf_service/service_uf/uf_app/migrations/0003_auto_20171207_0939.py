# Generated by Django 2.0 on 2017-12-07 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uf_app', '0002_auto_20171207_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uf',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]