# faceapp.urls
from django.urls import path

from .apis import FaceCompare

urlpatterns = [
    path('compare/', FaceCompare.as_view(), name='face_compare'),
]
