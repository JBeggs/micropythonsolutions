from django.contrib import admin

from .models import Content


class ContentAdmin(admin.ModelAdmin):
    list_display = ("creator", "name", "short_description",  "image_tag", 'created_at',)


admin.site.register(Content, ContentAdmin)
