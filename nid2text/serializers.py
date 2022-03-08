# nid2text/serializers.py
from drf_base64.serializers import ModelSerializer

from .models import NIDCardStorageModel


class NIDCardStorageModelSerializer(ModelSerializer):
    class Meta:
        model = NIDCardStorageModel
        fields = [
            'id',
            'image',
        ]
