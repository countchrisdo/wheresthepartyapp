from django.forms import ModelForm
from .models import Comment, Rating

class RatingForm(ModelForm):
  class Meta:
    model = Rating
    fields = ['rating']

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']
