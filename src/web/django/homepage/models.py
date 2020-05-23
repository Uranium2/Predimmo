from django.db import models


# Create your models here.
class Search(models.Model):
    prix = models.IntegerField()

    def __str__(self):
        return self.prix
