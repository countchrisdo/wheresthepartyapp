from django.contrib import admin
#import models
from .models import *


# Register your models here.
admin.site.register(Event)
admin.site.register(Comment)

