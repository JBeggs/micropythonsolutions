from cms.app_base import CMSApp
from cms.models import Page
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.conf import settings
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView


from api.models import Content, Message

from PIL import Image


@login_required
def update_content(request):

    if request.POST:

        image = {
            key: value for key, value in request.POST.items()
            if 'textarea_editor_'.lower() in key.lower()
        }
        name = {
            key: value for key, value in request.POST.items()
            if 'image_content_editor_'.lower() in key.lower()
        }
        desc = ''
        if bool(image):
            desc = image[next(iter(image))]

        if bool(name):
            name = next(iter(name)).replace('image_content_editor_', '')
        else:
            name = next(iter(image)).replace('textarea_editor_', '')

        content = Content.objects.filter(name=name).first()

        for key, in_memory_file in request.FILES.items():
            content.image = in_memory_file

        content.desc = desc
        if request.user.is_staff:
            content.save()

    else:
        partial_key = 'textarea_editor_'

        matching_items = {
            key: value for key, value in request.GET.items()
            if partial_key.lower() in key.lower()
        }

        for element, content in matching_items.items():
            name = element.replace(partial_key, "")
            element_content = Content.objects.filter(name=name).first()
            element_content.desc = content
            if request.user.is_staff:
                element_content.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, id):

    if id:
        delete = Content.objects.filter(pk=id).first()
        if request.user == delete.creator:
            delete.delete()

    return redirect(request.META.get('HTTP_REFERER'))


def save_message(request):
    error = ''
    try:
        message = Message()
        message.name = mark_safe('')
        message.email = mark_safe('')
        message.message = mark_safe('')
        message.save()
    except:
        error = ''

    return redirect(request.META.get('HTTP_REFERER') + f'?error={error}')
