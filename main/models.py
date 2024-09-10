from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.title
