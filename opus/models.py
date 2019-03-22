from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
  def get_query(self):
    return super(PublishedManager, self).get_query().filter(status='published')

class ContentPost(models.Model):
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published')
  )
  title       = models.CharField(max_length=250)
  slug        = models.SlugField(max_length=250, unique_for_date='publish')
  author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
  body        = models.TextField()
  publish     = models.DateTimeField(default=timezone.now)
  created     = models.DateTimeField(auto_now_add=True)
  updated     = models.DateTimeField(auto_now=True)
  status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
  objects     = models.Manager()
  published   = PublishedManager()

  def get_absolute_url(self):
      return reverse("opus:magum_opus", args=[self.slug])
  

  class Meta:
    ordering = ('-publish',)

  def __str__(self):
    return self.title

class Comment(models.Model):
  contentpost  = models.ForeignKey(ContentPost, on_delete=models.CASCADE, related_name='comments')
  name         = models.CharField(max_length=80)
  email        = models.EmailField() 
  body         = models.TextField()
  created      = models.DateTimeField(auto_now_add=True)
  updated      = models.DateTimeField(auto_now=True)
  active       = models.BooleanField(default=True)

  class Meta:
    ordering = ('created',)

  def __str__(self):
    return 'Comment by {} on {}'.format(self.name, self.contentpost)