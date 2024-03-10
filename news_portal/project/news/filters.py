import django_filters
from django import forms

from .models import NewsPost, Category

# Создаем свой набор фильтров для модели NewsPost.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class NewsPostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок',
                                      widget=forms.TextInput(attrs={'placeholder': 'Поиск по названию'}))
    category = django_filters.ModelChoiceFilter(field_name='category', empty_label='Все категории',
                                                    label='Категория', queryset=Category.objects.all())
    date_pub = django_filters.DateFilter(field_name='date_pub', lookup_expr='gte', label='Дата',
                                             widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
        model = NewsPost
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = ['title','category','date_pub']