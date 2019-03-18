from django.urls import path
from . import views

app_name = 'opus'

urlpatterns = [
    #contentpost views
    path('', views.list_opus, name='list_opus'),
    path('<int:year>/<int:month>/<int:day>/<slug:contentpost>/', views.magum_opus, name='magum_opus'),
]
