from django.db import models
from django.urls import reverse


class NewsPost(models.Model):
    title = models.CharField(
        max_length=64,
        unique=True,# названия новости не должны повторяться
    )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='newspost',)  # все новости в категории будут доступны через поле
    Text = models.TextField()
    date_pub = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.title}: {self.category}: {self.Text[:20]} : {self.date_pub}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


# Категория, к которой будет привязываться Новость
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name.title()

