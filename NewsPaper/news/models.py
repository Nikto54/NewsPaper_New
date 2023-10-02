from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum



class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author_post=self.id).aggregate(rating=Coalesce(Sum('rating'), 0))[
                          'rating'] * 3
        comment_rating = \
        Comment.objects.filter(user_comment=self.author_user).aggregate(rating=Coalesce(Sum('rating'), 0))[
            'rating']
        rating_posts = \
        Comment.objects.filter(post_comment__author_post=self.id).aggregate(rating=Coalesce(Sum('rating'), 0))[
            'rating']

        self.rating = post_rating + comment_rating + rating_posts
        self.save()


class Category(models.Model):
    title_category = models.CharField(max_length=255, unique=True)
    subscribers=models.ManyToManyField(User,blank=True,null=True)

    def __str__(self):
        return self.title_category
class Post(models.Model):
    CHOICES = [
        ('article', 'Статья'),
        ('news', 'Новость'),
    ]
    title = models.CharField(max_length=255)
    text = models.TextField()
    author_post = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    categories_post = models.ManyToManyField(Category, through='PostCategory')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title+':'+self.text[:24]


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()




class PostCategory(models.Model):
    post_category = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_post = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(default='')
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()