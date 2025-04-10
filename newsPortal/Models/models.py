from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг статей автора, умноженный на 3
        post_rating = sum(post.rating for post in self.post_set.all()) * 3

        # Суммарный рейтинг всех комментариев автора
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(user=self.user))

        # Суммарный рейтинг всех комментариев к статьям автора
        comments_to_posts_rating = sum(
            comment.rating for post in self.post_set.all() for comment in Comment.objects.filter(post=post)
        )

        # Обновляем рейтинг автора
        self.rating = post_rating + comment_rating + comments_to_posts_rating
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    article = 'AR'
    news = 'NE'

    CHOICE = [
        (article, 'Статья'),
        (news, 'Новости')
    ]

    choice = models.CharField(max_length=2, choices=CHOICE)
    datatime_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.heading}: {self.text[:30]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_com = models.TextField()
    datetime_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
