from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from utils import get_password


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Регистрация', 'button': 'Сохранить'}
    success_url = reverse_lazy('users:confirm_mail')

    def form_valid(self, form):
        verified_password = get_password()
        form.verified_password = verified_password
        new_user = form.save()
        new_user.verified_password = verified_password

        send_mail(
            subject='Поздравляем с регистрацией!',
            message=f'Чтобы завершить регистрацию, '
                    f'перейдите по ссылке: http://127.0.0.1:8000/user/verifying?code={new_user.verified_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


def confirm_mail(request):
    context = {'title': 'Пожалуйста, подтвердите почту.',
               'text': 'Для окончания регистрации Вам нужно пройти по ссылке в письме, '
                       'которое было отправлено Вам на указанный e-mail.'}
    return render(request, 'users/information.html', context)


def verify_view(request):
    code = request.GET.get('code')
    user = User.objects.get(verified_password=code)
    user.verified = True
    user.save()
    context = {'title': 'Добро пожаловать!',
               'text': 'Почта успешно подтверждена'}
    return render(request, 'users/information.html', context)


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


def login_fail(request):
    return render(request, 'users/login_fail.html')


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/login.html'
    extra_context = {'title': 'Сброс пароля',
                     'button': 'Отправить',
                     'text': 'Введите свой e-mail, указанный в профиле.'}
    success_url = reverse_lazy('users:reset_done')

    def form_valid(self, form):
        password = get_password()
        user_mail = form.cleaned_data.get('email')

        try:
            user = User.objects.get(email=user_mail)
            user.set_password(password)
            user.save()
            send_mail(
                subject='Сброс пароля',
                message=f'Ваш новый пароль: {password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_mail]
            )
            return super().form_valid(form)

        except ObjectDoesNotExist:
            return redirect(reverse('users:wrong_mail'))


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/information.html'
    extra_context = {'title': 'Письмо с инструкциями по восстановлению пароля отправлено',
                     'text': 'Мы отправили вам письмо с новым паролем на указанный адрес'
                             ' электронной почты (если в нашей базе данных есть такой адрес). '
                             'Вы должны получить ее в ближайшее время. Если вы не получили письмо, пожалуйста, '
                             'убедитесь, что вы ввели адрес с которым Вы зарегистрировались, '
                             'и проверьте папку со спамом.'}


def wrong_mail(request):
    context = {'title': 'Пользователь с указанной почтой не найден',
               'text': 'Пожалуйста, проверьте корректность введённой почты, либо зарегистрируйтесь, '
                       'используя указанную почту.'}
    return render(request, 'users/information.html', context)
