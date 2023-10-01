from django.urls import path

from .views import PostList,PostView,PostSearch,PostCreate,PostEdit,PostDelete


urlpatterns = [
   path('<int:pk>',PostView.as_view()),
   path('', PostList.as_view(),name='post_list'),
   path('search/',PostSearch.as_view()),
   path('create/',PostCreate.as_view()),
   path('<int:pk>/edit',PostEdit.as_view()),
   path('<int:pk>/delete',PostDelete.as_view())

]