from django.urls import path

from catalog.apps import MainConfig
from catalog.views import *

app_name = MainConfig.name

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='edit_product'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
]
