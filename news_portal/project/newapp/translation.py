from .models import Category, Post
from modeltranslation.translator import register, TranslationOptions # импортируем декоратор для перевода и класс


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text', 'postCategory') # указываем, какие именно поля надо переводить в виде кортежа