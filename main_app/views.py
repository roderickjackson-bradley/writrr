from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from.models import Writrr, Readrr, Opu
from.forms import CommentForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'writrr'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid credentials - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class WritrrCreate (LoginRequiredMixin, CreateView):
    model = Writrr
    fields = ['title', 'email', 'bio', 'created']

    def form_valid(self, form):
      # Assign the logged in user
      form.instance.user = self.request.user
      # Let the CreateView do its job as usual
      return super().form_valid(form)

class WritrrUpdate (LoginRequiredMixin, UpdateView):
    model = Writrr
    fields = ['email', 'title', 'bio']

class WritrrDelete (LoginRequiredMixin, DeleteView):
    model = Writrr
    success_url = '/writrrs/'

# Create your views here.
def home (request):
    return render (request, 'home.html')

def about (request):
    return render(request, 'about.html')

@login_required
def writrrs_index(request):
    writrrs = Writrr.objects.filter(user=request.user)
    return render (request, 'writrrs/index.html', { 'writrrs': writrrs })

@login_required
def writrrs_detail(request, writrr_id):
    writrr = Writrr.objects.get(id=writrr_id)
    readrrs_writrr_doesnt_have = Readrr.objects.exclude(id__in = writrr.readrrs.all().values_list('id'))
    comment_form = CommentForm()
    return render (request, 'writrrs/detail.html', { 
      'writrr': writrr, 
      'comment_form':comment_form,
      'readrrs': readrrs_writrr_doesnt_have
      })

@login_required
def add_comment(request, writrr_id):
      # create the ModelForm using the data in request.POST
  form = CommentForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_comment = form.save(commit=False)
    new_comment.writrr_id = writrr_id
    new_comment.save()
  return redirect('detail', writrr_id=writrr_id)

@login_required
def add_opu(request, writrr_id):
	# opu-file was the "name" attribute on the <input type="file">
  opu_file = request.FILES.get('opu-file', None)
  if opu_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
    key = uuid.uuid4().hex[:6] + opu_file.name[opu_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(opu_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to cat_id or cat (if you have a cat object)
      opu = Opu(url=url, writrr_id=writrr_id)
      opu.save()
    except:
      print('An error occurred uploading file to S3')
  return redirect('detail', writrr_id=writrr_id)

@login_required
def assoc_readrr(request, writrr_id, readrr_id):
  Writrr.objects.get(id=writrr_id).readrrs.add(readrr_id)
  return redirect('detail', writrr_id=writrr_id)

@login_required
def unassoc_readrr(request, writrr_id, readrr_id):
  Writrr.objects.get(id=writrr_id).readrrs.remove(readrr_id)
  return redirect('detail', writrr_id=writrr_id)

class ReadrrList(LoginRequiredMixin, ListView):
  model = Readrr

class ReadrrDetail(LoginRequiredMixin, DetailView):
  model = Readrr

class ReadrrCreate(LoginRequiredMixin, CreateView):
  model = Readrr
  fields = '__all__'

class ReadrrUpdate(LoginRequiredMixin, UpdateView):
  model = Readrr
  fields = ['caption', 'email']

class ReadrrDelete(LoginRequiredMixin, DeleteView):
  model = Readrr
  success_url = '/readrrs/'