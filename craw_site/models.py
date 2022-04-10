from django.db import models

# Create your models here.
class Crawdata(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목"),
    link = models.URLField()