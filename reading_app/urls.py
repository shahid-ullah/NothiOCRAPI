from django.contrib import admin
from .views import read_view, OCRAPIView
from django.urls import path,include

urlpatterns = [

    # path('',read_view,name="reading_img"),
    path('NothiOCRApi/', OCRAPIView.as_view(), name="api")
]
