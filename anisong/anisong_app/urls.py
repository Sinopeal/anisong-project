from django.urls import path

from .views import *
from django.views.generic.base import TemplateView

urlpatterns = [
        path('', TemplateView.as_view(template_name="index.html")),
        path('songs/',get_rec_songs)
]

