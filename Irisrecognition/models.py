from django.db import models

# Create your models here.

class PictureUpload(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images_upload', blank=True, null=True)
    identified_image = models.ImageField(upload_to='identified_images_upload', blank=True, null=True)