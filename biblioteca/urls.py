from django.urls import path
from biblioteca.views import index, inicio

urlpatterns = [
    path('', index),
    path('inicio/', inicio, name="inicio")
]
