from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import MainConfig
from catalog.views import *

app_name = MainConfig.name

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('<int:pk>/products/', category_products, name='category_product'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='edit_product'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete_product'),
    path('moderation/<int:pk>', ModeratorProductUpdateView.as_view(), name='moderate_product'),
    path('categories/', categories, name='categories')
]
