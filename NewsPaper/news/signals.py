from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper.settings import EMAIL_HOST_USER
from news.models import  PostCategory

def send_notification(preview,pk,title,subscribers):
    html_content =render_to_string(
        'post_created_email.html',
        {
            'text': preview
        }
    )
    msg=EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=EMAIL_HOST_USER
    )
    msg.attach_alternative(html_content,'text/html')
    msg.send()
@receiver(m2m_changed,sender=PostCategory)
def notify_about_new_post(sender,instance,**kwargs):
    if kwargs['action']=='post_add':
        categories = instance.category.all()
        subscribers_email =[]

        for cat in categories:
            subscribers= cat.subscribers.all()
            subscribers_email+=[s.email for s in subscribers]


    send_notification(instance.preview,instance.pk,instance.title,subscribers_email)