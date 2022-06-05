# faceapp/serializers.py
from drf_base64.fields import Base64ImageField
from rest_framework import serializers


class FaceCompareSerializer(serializers.Serializer):
    nidcard_image = Base64ImageField()
    webcam_image = Base64ImageField()
