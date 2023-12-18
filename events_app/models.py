from django.db import models


# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=250)
    discount = models.PositiveIntegerField(default=25)

    def __str__(self):
        return str(self.title) + ' - ' + str(self.discount) + '%'
