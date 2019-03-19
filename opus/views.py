from django.shortcuts import render, get_object_or_404
from .models import ContentPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


def list_opus(request):
  object_list = ContentPost.published.all()
  paginator = Paginator(object_list, 3) #List only three post per page
  page = request.GET.get('page', 1)
  try:
    contentposts = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer deliver the first page
    contentposts = paginator.page(1)
  except EmptyPage:
    # If page is out of range deliver last page of results
    contentposts = paginator.page(paginator.num_pages)
  return render (request, 'opus/contentpost/index.html', {'page': page, 'contentposts': contentposts})

def magum_opus(request, contentpost):
  contentpost = get_object_or_404(ContentPost, 
  slug=contentpost)
  return render(request, 'opus/contentpost/show.html', {'contentpost': contentpost})

class ContentPostListView(ListView):
  queryset = ContentPost.published.all()
  context_object_name = 'contentpost'
  paginate_by = 3
  template_name = 'opus/contentpost/index.html'