from django.contrib import admin
from .models import *

admin.site.register([Category, Restaurant, Review, Comment, Reply, Like])


