from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3 
import os
from .models import Event 

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def events_index(request):
  events = Event.objects.all()
  return render(request, 'events/index.html', {'events': events})

class EventDetail(DetailView):
  model = Event

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