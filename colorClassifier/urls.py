from django.urls import path, include

# from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("get_color_tags", views.get_color_tags),
    path("get_colors", views.get_colors),
    path("get_complete_color", views.get_complete_color),
    path("changeColor", views.changeColor),
]
