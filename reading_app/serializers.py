# reading_app/serializers.py

# third party import
from rest_framework import serializers

# local import
from .models import UploadImage


class UploadImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadImage
        fields = ['image', 'language',]
