# Generated by Django 3.2 on 2022-10-12 18:47

from django.db import migrations, models
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rpa', '0003_auto_20220925_1019'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iehporder',
            options={'get_latest_by': 'modified'},
        ),
        migrations.AlterModelOptions(
            name='opticalpiaorder',
            options={'get_latest_by': 'modified'},
        ),
        migrations.AddField(
            model_name='iehporder',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='iehporder',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='opticalpiaorder',
            name='confirmation_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='opticalpiaorder',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='opticalpiaorder',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='opticalpiaorder',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='uploaded-pdf/optical-pia/'),
        ),
    ]
