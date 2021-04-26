# digit_recognizer/apps.py
import os

from django.apps import AppConfig
from django.conf import settings
from keras.models import load_model


class DigitRecognizerConfig(AppConfig):
    name = 'digit_recognizer'

    # model_path = os.path.join(settings.DIGIT_RECOGNIZER_MODEL, 'abcde.h5')
    model_path = os.path.join(settings.DIGIT_RECOGNIZER_MODEL, 'nuraz_single_canvas_50.h5')
    model_HCR = load_model(model_path)
