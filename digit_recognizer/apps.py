from django.apps import AppConfig

from keras.models import model_from_json,load_model
import os
from django.conf import settings

class DigitRecognizerConfig(AppConfig):
    name = 'digit_recognizer'

    model_path = os.path.join(settings.MODELS, 'abcde.h5')
    model_HDR = load_model(model_path)
