from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import PostCategory, Post, Category
from celery import shared_task
from django.utils import timezone
from datetime import datetime, timedelta

from NewsPaper import settings


@shared_task()
def send_notifications(pk):
    post = Post.objects.get(pk=pk)
    categories=post.categories_post.all()
    subscribers_emails = []
    title=post.title
    for cat in categories:
        subscribers=cat.subscribers.all()
        subscribers_emails+=[s.email for s in subscribers]
    html_content= render_to_string(
        'post_created_email.html',
        {
            'text':title,
            'link':f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='Nikto51@yandex.ru',
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content,'text/html')
    msg.send()


@shared_task()
def send_weekly_mail():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    categories = set(posts.values_list('categories_post__title_category', flat=True))
    subscribers = set(Category.objects.filter(title_category__in=categories).values_list('subscribers__email',flat=True))
    html_content = render_to_string(
        'daily_post.html', {
            'link': settings.SITE_URL + '/news/',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('ok')
