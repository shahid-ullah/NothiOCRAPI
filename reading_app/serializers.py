# reading_app/serializers.py

# third party import
from rest_framework import serializers
from drf_base64.serializers import ModelSerializer

# local import
from .models import UploadImage


class UploadImageSerializer(ModelSerializer):

    class Meta:
        model = UploadImage
        fields = ['image', 'language',]
