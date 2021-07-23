from django.db import models
from django.db.models.enums import Choices
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.db.models.fields import CharField, IntegerField, TextField
# from django.forms.widgets import Textarea
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django_gravatar.helpers import get_gravatar_url, has_gravatar, get_gravatar_profile_url, calculate_gravatar_hash

RATINGS = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

AGERATINGS = (
    ('General Admission', 'General Admission'),
    ('Teens 13+', 'Teens 13+'),
    ('Adults 18+', 'Adults 18+'),
    ('Adults 21+', 'Adults 21+')
)

PROTOCOL = (
    ('Nothing Specified', 'Nothing Specified'),
    ('Vaccination Required', 'Vaccination Required'),
    ('Mask Required Indoors', 'Mask Required Indoors'),
    ('Vaccination and Masks Required Indoors', 'Vaccination and Masks Required Indoors'),
)    

# Create your models here.

class Event(models.Model):
    event_name = CharField(max_length=200)
    address = CharField(max_length=200)
    description = TextField(max_length=500)
    date = models.DateField(auto_now=False, auto_now_add=False)
    hours_of_op = CharField(max_length=150,default='7:30am - 9:30pm')

    covid_protocol = models.CharField(
        'Covid Protocol',
        max_length=50,
        choices=PROTOCOL,
        default='Nothing Specified'
        )

    admission_fee = models.CharField(max_length=100,default='$5.00')

    age_rating = models.CharField(
        'Age Rating',
        max_length=50,
        choices=AGERATINGS,
        default=AGERATINGS[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name 

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

    class Meta:
        ordering = ['-date']

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

class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"
