from django.contrib import admin


from .models import UploadImage


class UploadImageAdmin(admin.ModelAdmin):
    list_display = ['language', 'image', 'text',]

admin.site.register(UploadImage, UploadImageAdmin)
