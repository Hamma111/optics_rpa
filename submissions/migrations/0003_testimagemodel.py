# Generated by Django 3.2 on 2022-08-15 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0002_auto_20220814_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='test-image/%Y/%m/')),
            ],
        ),
    ]