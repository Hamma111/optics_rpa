# Generated by Django 3.2 on 2022-08-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0004_auto_20220816_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opticalpiaordersubmission',
            name='error_screenshot',
            field=models.ImageField(blank=True, null=True, upload_to='error-screenshot/%Y-%m/'),
        ),
        migrations.AlterField(
            model_name='opticalpiaordersubmission',
            name='error_text',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='opticalpiaordersubmission',
            name='screenshot1',
            field=models.ImageField(blank=True, null=True, upload_to='optical-screenshot1/%Y-%m/'),
        ),
        migrations.AlterField(
            model_name='opticalpiaordersubmission',
            name='screenshot2',
            field=models.ImageField(blank=True, null=True, upload_to='optical-screenshot2/%Y-%m/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(upload_to='uploaded-csv/%Y-%m/'),
        ),
    ]