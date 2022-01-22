from django.urls import path
from . import views
urlpatterns = [
  path('scrape/', views.scrape, name="scrape"),
  path('', views.news_list, name="home"),
]