# Generated by Django 2.2.2 on 2019-06-24 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_auto_20190618_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='seats',
            field=models.IntegerField(default=0),
        ),
    ]