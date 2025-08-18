from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('publish', 'PUBLISHED'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='posts'
    )
    
    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
        
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'{self.name} added a comment at {self.created}'
    
    
    
