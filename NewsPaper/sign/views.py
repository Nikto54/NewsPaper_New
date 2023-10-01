from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


from .models import BaseRegisterForm


# Create your views here.
class BaseRegisterView(CreateView):
    model=User
    success_url = '/'
    form_class = BaseRegisterForm


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')