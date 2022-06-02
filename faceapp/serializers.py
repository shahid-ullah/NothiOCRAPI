# faceapp/serializers.py
from rest_framework import serializers


class FaceCompareSerializer(serializers.Serializer):
    nidcard_image = serializers.ImageField()
    webcam_image = serializers.ImageField()
