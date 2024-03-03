from django.db import models
from django.core.validators import MinValueValidator


# Товар для нашей витрины
class NewsPost(models.Model):
    title = models.CharField(
        max_length=64,
        unique=True, # названия новости не должны повторяться
    )
    Text = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    # поле категории будет ссылаться на модель категории



    def __str__(self):
        return f'{self.title}: {self.Text[:20]} : {self.date_pub}'


# Категория, к которой будет привязываться Новость
# class CategoryNews(models.Model):
#     # названия категорий тоже не должны повторяться
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name.title()
