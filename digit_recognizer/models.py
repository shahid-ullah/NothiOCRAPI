from django.db import models

# Create your models here.
# model for api
class UploadImage(models.Model):
    """
    Store API reuested image and Image Text
    """
    image = models.ImageField(upload_to='images/')
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)
