from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

class PostTranslationAdmin(TranslationAdmin):
    model = Post

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostTranslationAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)