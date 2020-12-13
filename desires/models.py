from django.db import models
from django.contrib.auth.models import User

class Label(models.Model):
    name = models.CharField(max_length=20)
    count = models.IntegerField(default=0)

class Desire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=20)
    description = models.TextField(blank=True)
    url = models.URLField()
    image_url = models.URLField()
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateField(auto_now_add=True)