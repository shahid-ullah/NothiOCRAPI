# reading_app/urls.py
from django.urls import path

from .views import I2TNIDAPI, I2TNIDWeb, OCRAPIView

urlpatterns = [
    # path('',read_view,name="reading_img"),
    # path('NothiOCRApi/', OCRAPIView.as_view(), name="api")
    path('', OCRAPIView.as_view(), name="api"),
    path('nid/web/', I2TNIDWeb, name="i2tnid-web"),
    path('nid/', I2TNIDAPI.as_view(), name="i2tnid-api"),
]
