# single_digit_canvas/models.py
from django.db import models


class SingleDigitCanvasModel(models.Model):
    image = models.ImageField(upload_to='images_single_digit_canvas_api/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
