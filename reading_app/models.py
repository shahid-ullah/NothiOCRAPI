from django.db import models

# model for webview
class ImageUpload(models.Model):
    """
    Store requested image and image text from webview
    """
    lang_choice=(
        ('ben','Bangla'),
        ('eng','English'),
        ('ben+eng','Bangla & English')
    )
    image = models.ImageField(upload_to='images_ocr_web/')
    text =models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    # language=models.CharField(max_length=20,choices=lang_choice,default='bangla')
    language=models.CharField(max_length=20,choices=lang_choice,default='ben')

    class Meta:
        ordering=('-created',)

# model for api
class UploadImage(models.Model):
    """
    Store API reuested image and Image Text
    """
    lang_choice=(
        ('ben','Bangla'),
        ('eng','English'),
        ('ben+eng','Bangla & English')
    )
    image = models.ImageField(upload_to='images_ocr_api/')
    text =models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    language=models.CharField(max_length=20,choices=lang_choice,default='ben')

    class Meta:
        ordering=('-created',)

