from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Post


@receiver(post_save, sender=Post)
def product_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(
        subscriptions__category__in=instance.postCategory.all()
    ).values_list('email', flat=True)

    subject = f'Новый пост в категории {":".join(category.name for category in instance.postCategory.all())}'

    text_content = (
        f'Пост: {instance.title}\n'
        f'Категория: {instance.preview()}\n\n'
        f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
    )

    html_content = (
        f'Заголовок: {instance.title}<br>'
        f'Текст: {instance.preview}<br><br>'
        f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
        f'Перейти</a>'
    )

    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()