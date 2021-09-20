# reading_app/urls.py
from django.urls import path

from .views import I2TNID, OCRAPIView

urlpatterns = [
    # path('',read_view,name="reading_img"),
    # path('NothiOCRApi/', OCRAPIView.as_view(), name="api")
    path('', OCRAPIView.as_view(), name="api"),
    path('nid/', I2TNID, name="i2tnid"),
]
