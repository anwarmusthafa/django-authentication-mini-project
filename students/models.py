from django.db import models

# Create your models here.

class Students(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.name

