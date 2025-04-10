from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.

class PostListView(ListView):
    model = Post
    ordering = 'heading'
    template_name = 'Posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'post'
