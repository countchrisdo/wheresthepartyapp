from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.db.models import Avg
import uuid
import boto3 
import os
from .models import Event, Rating
from .forms import RatingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def events_index(request):
  events = Event.objects.all()
  for event in events:
    rating_avg = Rating.objects.filter(event_id=event.id).aggregate(Avg('rating'))
    event.rating_avg = rating_avg['rating__avg']
  return render(request, 'events/index.html', {'events': events})

class EventDetail(DetailView):
  model = Event
  
  def get_context_data(self, **kwargs):
    rating_form = RatingForm()
    rating_avg = Rating.objects.filter(event_id=self.kwargs['pk']).aggregate(Avg('rating'))
    context = super().get_context_data(**kwargs)
    context['rating_avg'] = rating_avg['rating__avg']
    context['rating_form'] = rating_form 
    
    return context 

class EventCreate(CreateView):
  model = Event
  fields = ['event_name', 'location', 'description']
  success_url = '/events'

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class EventUpdate(UpdateView):
  model = Event
  fields = '__all__'

class EventDelete(DeleteView):
  model = Event
  success_url = '/events/'

def add_rating(request, event_id):
  # create a ModelForm instance using the data in the posted form
  form = RatingForm(request.POST)
  # validate the data
  if form.is_valid():
    new_rating = form.save(commit=False)
    new_rating.event_id = event_id
    new_rating.save()
  return redirect('detail', event_id=event_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)