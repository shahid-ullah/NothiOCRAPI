# single_digit_canvas/serializers.py
from drf_base64.serializers import ModelSerializer

from .models import SingleDigitCanvasModel


class SingleDigitCanvasModelSerializer(ModelSerializer):
    class Meta:
        model = SingleDigitCanvasModel
        fields = [
            'image',
        ]
