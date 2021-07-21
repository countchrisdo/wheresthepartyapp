from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls.base import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
import uuid
import boto3 
import os
from .models import Comment, Event, Rating, Photo
from .forms import RatingForm, CommentForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def profile(request):
  events = Event.objects.filter(user=request.user)
  for event in events:
    rating_avg = Rating.objects.filter(event_id=event.id).aggregate(Avg('rating'))
    event.rating_avg = rating_avg['rating__avg']
  return render(request, 'accounts/profile.html', {'events': events})

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
    comment_form = CommentForm()
    rating_avg = Rating.objects.filter(event_id=self.kwargs['pk']).aggregate(Avg('rating'))
    context = super().get_context_data(**kwargs)
    context['rating_avg'] = rating_avg['rating__avg']
    context['rating_form'] = rating_form 
    context['comment_form'] = comment_form
    
    return context 

class EventCreate(LoginRequiredMixin, CreateView):
  model = Event
  fields = ['event_name', 'location', 'description','date','hours_of_op', 'covid_protocol', 'admission_fee', 'age_rating']
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

@login_required
def add_rating(request, event_id):
  # create a ModelForm instance using the data in the posted form
  form = RatingForm(request.POST)
  # validate the data
  if form.is_valid():
    new_rating = form.save(commit=False)
    new_rating.event_id = event_id
    new_rating.user_id = request.user.id
    new_rating.save()
  return redirect('detail', pk=event_id)

@login_required
def add_comment(request, event_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.event_id = event_id
    new_comment.user_id = request.user.id
    new_comment.save()
  return redirect('detail', pk=event_id)

class CommentUpdate(LoginRequiredMixin, UpdateView):
  model = Comment
  fields = ['comment']
  success_url = '/events/'

  def get_success_url(self):
    obj = self.get_object()
    return reverse('detail', kwargs={'pk': obj.event.id})

class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  success_url = '/events/'
  
  def get_success_url(self):
    obj = self.get_object()
    return reverse('detail', kwargs={'pk': obj.event.id})

class CommentDetail(DetailView):
    model = Comment
 
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.email = request.POST.get("email")
      user.save() 
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def add_photo(request, event_id):
  
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
        bucket = os.environ['S3_BUCKET']
        s3.upload_fileobj(photo_file, bucket, key)
        # build the full url string
        url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        Photo.objects.create(url=url, event_id=event_id)
    except:
        print('An error occurred uploading file to S3')
  return redirect('detail', pk=event_id)