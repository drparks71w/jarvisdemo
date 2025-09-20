from django.urls import path
from . import views

app_name = 'jarvis_chat'

urlpatterns = [
    path('', views.jarvis_view, name='jarvis'),
    path('ask/', views.ask_notebook, name='ask_notebook'),
]
