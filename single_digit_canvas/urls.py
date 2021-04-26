# single_digit_canvas/urls.py
from django.urls import path

from .views import NurazDigitCanvasAPI

urlpatterns = [
    path('', NurazDigitCanvasAPI.as_view(), name="nuraz_digit_canvas")
]
