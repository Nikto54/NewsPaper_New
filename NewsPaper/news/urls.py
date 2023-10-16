from django.urls import path
from django.views.decorators.cache import cache_page

from .views import PostList, PostView, PostSearch, PostCreate, PostEdit, PostDelete, CategoryListView, subscribe


urlpatterns = [
   path('<int:pk>',cache_page(300)(PostView.as_view())),
   path('', cache_page(300)(PostList.as_view()),name='post_list'),
   path('search/',PostSearch.as_view()),
   path('create/',PostCreate.as_view()),
   path('<int:pk>/edit',PostEdit.as_view()),
   path('<int:pk>/delete',PostDelete.as_view()),
   path('categories/<int:pk>/',CategoryListView.as_view()),
   path('categories/<int:pk>/subscribe/',subscribe,name='subscribe')

]