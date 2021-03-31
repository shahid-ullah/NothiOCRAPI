import os

from django.apps import AppConfig
from django.conf import settings
from keras.models import load_model, model_from_json


class DigitRecognizerConfig(AppConfig):
    name = 'digit_recognizer'

    model_path = os.path.join(settings.MODELS, 'abcde.h5')
    model_HDR = load_model(model_path)
