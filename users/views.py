from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Регистрация', 'button': 'Сохранить'}
    success_url = reverse_lazy('users:login')


class UserProfileView(DetailView):
    model = User
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class EditProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Редактирование профиля', 'button': 'Сохранить'}
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
