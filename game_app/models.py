from django.db import models
from category_app.models import Category
from brand_app.models import Brand
from events_app.models import Event


# Create your models here.

class Game(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    price = models.PositiveIntegerField()
    genre = models.ManyToManyField(Category)
    brand_name = models.ForeignKey(Brand, on_delete=models.SET_DEFAULT, default='unknown')
    release_at = models.DateField(null=True,blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True)
    is_free = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.title


