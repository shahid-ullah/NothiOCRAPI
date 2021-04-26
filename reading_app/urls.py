# reading_app/urls.py
from django.urls import path

from .views import OCRAPIView

urlpatterns = [
    # path('',read_view,name="reading_img"),
    # path('NothiOCRApi/', OCRAPIView.as_view(), name="api")
    path('', OCRAPIView.as_view(), name="api")
]
