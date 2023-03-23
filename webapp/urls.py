from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_blog_post, name='create_blog_post'),
    path('edit/',views.testview,name="testview"),
    path('getnbtinfo',views.getnbtinfo,name="getnbtinfo")
]