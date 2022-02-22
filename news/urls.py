from django.urls import path
from . import views
app_name = "news"
urlpatterns = [
  path('', views.home, name="home"),
  path('res', views.index, name="index")
]