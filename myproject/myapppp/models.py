from django.db import models

# Create your models here.
class cityname(models.Model):
    ticker=models.CharField(max_length=20)

    def __str__(self):
        return self.ticker
