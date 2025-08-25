from django.shortcuts import get_object_or_404, render
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(status='publish')
    
    return render(
        request,
        'blog/post/list.html',
        {
            'posts': posts
        }
    )
    
def post_detail(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        status='publish'
    )
    
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
        }
    )