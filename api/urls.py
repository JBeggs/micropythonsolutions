from django.contrib import admin
from django.urls import include, path

from api.views import update_content, delete, save_message

admin.autodiscover()

urlpatterns = [
    path(r'update_content', update_content, name='update_content'),
    path(r'delete/<id>', delete, name='delete'),
    path(r'save_message', save_message, name='save_message'),
]
