# ocr_project/urls.py
from django.conf import settings  # new
from django.conf.urls.static import static  # new
from django.contrib import admin
from django.urls import include, path  # new

urlpatterns = [
    path('admin12djfdj@/', admin.site.urls),
    path('apiImageToText/', include('reading_app.urls')),
    path('apiNurazDigitCanvas/', include('single_digit_canvas.urls')),
    path('apiHCR/', include('digit_recognizer.urls')),
    path('face/', include('faceapp.urls')),
    path('', include('nid2text.urls')),
]
if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
