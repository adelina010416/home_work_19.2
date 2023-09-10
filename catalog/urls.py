from django.urls import path
from catalog.views import home, contacts

app_name = 'home'
urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contacts, name='contacts')

]
