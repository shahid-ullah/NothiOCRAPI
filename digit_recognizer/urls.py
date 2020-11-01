from .views import DigitRecognizerView
from django.urls import path

urlpatterns = [
    path('', DigitRecognizerView.as_view(), name="api")
]