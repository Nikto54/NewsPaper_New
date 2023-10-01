from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Category,Author,Post,Comment
from .filters import PostFilter
from .forms import PostForm
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class PostSearch(ListView):
    model = Post
    template_name = 'PostSearch.html'
    context_object_name = 'search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
class PostList(ListView):
    model=Post
    ordering = 'date'
    template_name = 'PostList.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset=PostFilter(self.request.GET,queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset']=self.filterset
        return context

class PostView(DetailView):
    model=Post
    template_name='PostView.html'
    context_object_name='post'

class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'PostCreate.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'news' in self.request.path:
            type = 'news'
        elif 'articles' in self.request.path:
            type = 'article'
        self.object.type = type
        return super().form_valid(form)

class PostEdit(LoginRequiredMixin,UpdateView):
    model = Post
    template_name = 'PostEdit.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

class PostDelete(DeleteView):
    model = Post
    template_name = 'PostDelete.html'