# single_digit_canvas/urls.py
from django.urls import path

from .views import SingleDigitCanvasAPI

urlpatterns = [
    # path('',read_view,name="reading_img"),
    # path('NothiOCRApi/', OCRAPIView.as_view(), name="api")
    path('apiSingleDigitCanvas/', SingleDigitCanvasAPI.as_view(), name="single_digit_canvas")
]
