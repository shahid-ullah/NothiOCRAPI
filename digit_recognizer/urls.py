# digit_recognizer/urls.py
from django.urls import path

from .views import DigitRecognizerAPI

urlpatterns = [
    path('', DigitRecognizerAPI.as_view(), name="api"),
]
