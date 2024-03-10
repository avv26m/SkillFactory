from django.contrib import admin
from .models import NewsPost, Category


admin.site.register(NewsPost)
admin.site.register(Category)