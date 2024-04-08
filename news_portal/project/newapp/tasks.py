
import datetime

from celery import shared_task

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Subscription
from django.conf import settings

from datetime import timezone


@shared_task
def send_email_task(pk):
    post = Post.objects.get(pk=pk)
    subscribers_emails = User.objects.filter(subscriptions__category__in=post.postCategory.all()).values_list('email', flat=True)

    subject = f'Добавлена новая публикация {",".join(category.name for category in post.postCategory.all())}'

    text_content = (
            f'Заголовок: {post.title}\n'
            f'Текст: {post.preview()}\n\n'
            f'Url: http://127.0.0.1:8000{post.get_absolute_url()}')

    html_content = (
            f'Заголовок: {post.title}<br>'
            f'Текст: {post.preview()}<br><br>'
            f'<a href="http://127.0.0.1{post.get_absolute_url()}">'
            f'Url</a>')

    for email in subscribers_emails:
        msg = EmailMultiAlternatives(subject, text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def weekly_send_email_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)

    categories = set(posts.values_list('postCategory__name', flat=True))


    subscribers = set(Subscription.objects.filter(category__name__in=categories).values_list('user__email', flat=True))

    html_content = render_to_string('daily_post.html',
                                    {'link': settings.SITE_URL,
                                             'posts': posts})
    msg = EmailMultiAlternatives(
        subject="Публикации за неделю",
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers)

    msg.attach_alternative(html_content, 'text/html')
    msg.send()