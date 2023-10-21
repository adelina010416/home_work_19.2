from django.urls import path

from catalog.apps import MainConfig
from catalog.views import home, contacts, product

app_name = MainConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pid>', product, name='product')
]
