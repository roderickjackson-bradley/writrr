from django.shortcuts import render, get_object_or_404
from .models import ContentPost

def list_opus(request):
  contentposts = ContentPost.published.all()
  return render (request, 'opus/contentpost/index.html', {'contentposts': contentposts})

def magum_opus(request, year, month, day, contentpost):
  contentpost = get_object_or_404(ContentPost, 
  slug=contentpost, status='published', publish_year=year, publish_month=month, publish_day=day)

  return render(request, 'opus/contentpost/show.html', {'contentpost': contentpost})