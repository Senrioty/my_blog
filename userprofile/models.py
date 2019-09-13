from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avator/%Y%m%d', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return '<User: %s>' % self.user.username