# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from core import scrapper


class DownloaderConfig(AppConfig):
    name = 'downloader'
    username = 'crosz'
    password = '5098'
    download_directory = '/Users/crossrt/watch/'

    def ready(self):
        scrapper.init()
        scrapper.login()
