from django.contrib import admin
from .models import Blogpost, Contact, BlogpostComment
# Register your models here.
admin.site.register((Blogpost, BlogpostComment, Contact))
