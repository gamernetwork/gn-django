# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 16:00
from __future__ import unicode_literals

from django.db import migrations, models
import gn_django.fields
import gn_django.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FieldValidatorExample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube', gn_django.fields.YoutubeField(blank=True, help_text='The <pre>YoutubeField</p> includes the <pre>YoutubeValidator</pre> by default.', max_length=255, null=True)),
                ('youtube_validator', models.CharField(blank=True, help_text='This is a regular old <pre>CharField</pre>, but has the <pre>YoutubeValidator</pre> assigned to it.', max_length=255, null=True, validators=[gn_django.validators.YoutubeValidator()])),
                ('gn_image_validator', models.CharField(blank=True, help_text="This is a regular old <pre>CharField</pre>, but still has the <pre>GamerNetworkImageValidator()</pre> assigned to it, and so only accepts images from Gamer Network's CDN.", max_length=255, null=True, validators=[gn_django.validators.GamerNetworkImageValidator()])),
            ],
        ),
    ]
