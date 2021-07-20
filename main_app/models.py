from django.db import models
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.db.models.fields import CharField, IntegerField, TextField
# from django.forms.widgets import Textarea
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

RATINGS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

# Create your models here.

# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Photo for event_id: {self.event_id} @{self.url}"

class Event(models.Model):
    event_name = CharField(max_length=200)
    location = CharField(max_length=200)
    description = TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # event_date = models.DateField(auto_now=False, auto_now_add=False)
    

    def __str__(self):
        return self.event_name 

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

    # class Meta:
    #     ordering = ['-event_date']

class Comment(models.Model):
    comment = TextField(max_length=280)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('comments_detail', kwargs={'pk': self.id})

class Rating(models.Model):
    rating = models.IntegerField(
        choices=RATINGS,
        default=RATINGS[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
