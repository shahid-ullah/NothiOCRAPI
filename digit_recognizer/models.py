from django.db import models

# Create your models here.
# model for api
class StoreImageForHCR(models.Model):
    """
    Store API reuested image and Image Text
    """
    image = models.ImageField(upload_to='images_hcr_api/')
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-created',)
