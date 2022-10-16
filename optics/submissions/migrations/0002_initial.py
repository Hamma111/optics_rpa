# Generated by Django 3.2 on 2022-10-16 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rpa', '0001_initial'),
        ('submissions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='submissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='opticalpiaordersubmission',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='optical_pia_submission', to='rpa.opticalpiaorder'),
        ),
        migrations.AddField(
            model_name='opticalpiaordersubmission',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='optical_pia_submissions', to='submissions.submission'),
        ),
        migrations.AddField(
            model_name='iehpordersubmission',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='iehp_submission', to='rpa.iehporder'),
        ),
        migrations.AddField(
            model_name='iehpordersubmission',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='iehp_submission', to='submissions.submission'),
        ),
    ]
