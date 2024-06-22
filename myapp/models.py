from django.db import models

class PostedImage(models.Model):
    image_url = models.URLField(unique=True)
    posted_at = models.DateTimeField(auto_now_add=True)