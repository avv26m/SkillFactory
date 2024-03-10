from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, Search, NewsCreate, NewsUpdate, NewsDelete


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='post_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', NewsDetail.as_view(), name='post_detail'),
   path('search/', Search.as_view(), name='search'),
   path('create/', NewsCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
]