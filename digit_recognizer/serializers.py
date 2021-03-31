# reading_app/serializers.py

# third party import
from drf_base64.serializers import ModelSerializer

# local import
from .models import StoreImageForHCR


class UploadImageSerializer(ModelSerializer):
    class Meta:
        model = StoreImageForHCR
        fields = [
            'image',
        ]
