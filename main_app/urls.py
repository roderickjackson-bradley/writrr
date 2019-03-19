from django.urls import path, include
from.import views

urlpatterns = [
 path('', views.home, name='home'),
 path('about/', views.about, name='about'),
 path('writrrs/', views.writrrs_index, name='index'),
 path('writrrs/<int:writrr_id>/', views.writrrs_detail, name='detail'),
 path('writrrs/create/', views.WritrrCreate.as_view(), name='writrrs_create'),
 path('writrrs/<int:pk>/update/', views.WritrrUpdate.as_view(), name='writrrs_update'),
 path('writrrs/<int:pk>/delete/', views.WritrrDelete.as_view(), name='writrrs_delete'),
 path('writrrs/<int:writrr_id>/add_comment/', views.add_comment, name='add_comment'),
 path('writrrs/<int:writrr_id>/add_opu/', views.add_opu, name='add_opu'),

 path('writrrs/<int:writrr_id>/assoc_readrr/<int:readrr_id>/', views.assoc_readrr, name='assoc_readrr'),
 path('writrrs/<int:writrr_id>/unassoc_readrr/<int:readrr_id>/', views.unassoc_readrr, name='unassoc_readrr'),
 path('readrrs/', views.ReadrrList.as_view(), name='readrrs_index'),
 path('readrrs/<int:pk>/', views.ReadrrDetail.as_view(), name='readrrs_detail'),
 path('readrrs/create/', views.ReadrrCreate.as_view(), name='readrrs_create'),
 path('readrrs/<int:pk>/update/', views.ReadrrUpdate.as_view(), name='readrrs_update'),
 path('readrrs/<int:pk>/delete/', views.ReadrrDelete.as_view(), name='readrrs_delete'),
 path('accounts/', include('django.contrib.auth.urls')),
 path('accounts/signup', views.signup, name='signup'),
]