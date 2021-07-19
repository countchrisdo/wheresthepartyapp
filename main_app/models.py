from django.db import models
from django.urls import reverse
from django.db.models.fields import CharField, IntegerField, TextField
# from django.forms.widgets import Textarea
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Photo for event_id: {self.event_id} @{self.url}"

class Event(models.Model):
    event_name = CharField(max_length=200)
    # comment = TextField(max_length=500)
    location = CharField(max_length=200)
    # rating = IntegerField(default=5)
    description = TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.event_name 

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

class Comment(models.Model):
    comment = TextField(max_length=280)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Rating(models.Model):
    rating = IntegerField(default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)





