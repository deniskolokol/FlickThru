# -*- coding: utf-8 -*-
"""
Module contains management command for loading images data.
"""
from __future__ import unicode_literals
import random
import urllib2

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from core.models import TitledImage
from mysql import connector


class Command(BaseCommand):
    """A management command which fills images data."""
    help = 'Fill database with images data'

    def handle(self, *args, **kwargs):
        cnx = connector.connect(user='root', password='pwd',
                                host='127.0.0.1', database='flickthru')
        cursor = cnx.cursor()
        request = \
            "select * from real_update limit 100"
        cursor.execute(request)
        values = cursor.fetchall()
        # TitledImage.objects.all().delete()
        for value in values:
            if value[7][-4:] == '.mp4':
                continue
            try:
                urllib2.urlopen(value[7])
            except urllib2.HTTPError:
                continue
            try:
                TitledImage.objects.create(
                    id=value[0], subscription_id=value[1], object_id=value[2],
                    subscription_object=value[3], media_username=value[4],
                    media_profile_picture=value[5], media_user_id=value[6],
                    media_standard_resolution_url=value[7],
                    media_like_count=value[8], media_id=value[9]
                )
            except IntegrityError:
                TitledImage.objects.create(
                    subscription_id=value[1], object_id=value[2],
                    subscription_object=value[3], media_username=value[4],
                    media_profile_picture=value[5], media_user_id=value[6],
                    media_standard_resolution_url=value[7],
                    media_like_count=value[8], media_id=value[9]
                )
            """
            if random.choice([0,1]):
                TitledImage.objects.create(
                    subscription_id=value[1], object_id=value[2],
                    subscription_object=value[3], media_username=value[4],
                    media_profile_picture=value[5], media_user_id=value[6],
                    media_standard_resolution_url=value[7],
                    media_like_count=value[8], media_id=value[9],
                     title=value[7]
                )
            else:
                TitledImage.objects.create(
                    subscription_id=value[1], object_id=value[2],
                    subscription_object=value[3], media_username=value[4],
                    media_profile_picture=value[5], media_user_id=value[6],
                    media_standard_resolution_url=value[7],
                    media_like_count=value[8], media_id=value[9]
                )
            """
        cnx.close()
