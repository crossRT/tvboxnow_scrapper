# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import core.scrapper as scrapper


def index(request):
    return HttpResponse('Downloader Index')


def drama_index(request):
    items = scrapper.get_drama_index()
    context = {
        'items': items
    }
    return render(request, 'index.html', context)


def drama_show(request, link):
    items = scrapper.get_drama_show(link)
    context = {
        'items': items
    }
    return render(request, 'show.html', context)


def drama_download(request, link):
    full_link = f"attachment.php?aid={request.GET.get('aid')}&k={request.GET.get('k')}&t={request.GET.get('t')}&sid={request.GET.get('sid')}"
    scrapper.get_drama_download(full_link)
    return HttpResponse(link)
