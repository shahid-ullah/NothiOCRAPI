from django.db import models


class NIDCardStorageModel(models.Model):
    """
    store NID card images.
    """

    image = models.ImageField(upload_to='nid_cards/')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
