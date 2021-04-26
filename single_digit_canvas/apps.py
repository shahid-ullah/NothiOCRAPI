# single_digit_canvas/apps.py
import os

from django.apps import AppConfig
from django.conf import settings

# from keras.models import load_model


class SingleDigitCanvasConfig(AppConfig):
    name = 'single_digit_canvas'
    model_path = os.path.join(settings.SINGLE_DIGIT_CANVAS_MODEL, 'nuraz_single_canvas_50.h5')
    # model = load_model(model_path)
