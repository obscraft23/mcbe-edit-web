from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_upload, name='index_upload'),
    path('edit/',views.editorview,name="editorview"),
    path('getnbtinfo',views.getnbtinfo,name="getnbtinfo")
]