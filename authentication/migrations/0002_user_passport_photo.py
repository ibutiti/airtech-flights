# Generated by Django 2.2.2 on 2019-06-14 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='passport_photo',
            field=models.ImageField(blank=True, null=True, upload_to='passport_photos'),
        ),
    ]