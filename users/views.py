from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView
from django.conf import settings

from users.forms import LoginForm, UserRegisterForm
from users.models import User
from users.tasks import send_activation_email


class UserLoginView(LoginView):
    model = User
    form_class = LoginForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm  # Переопределяем стандартную форму UserCreationForm на свою
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.verification_token = get_random_string(30)
        send_activation_email.delay(
            self.object.email,
            f'Здравствуйте!\nНажмите на ссылку ниже для активации вашей учетной записи\n'
            f'http://{get_current_site(self.request)}/users/confirm/{self.object.verification_token}')
        return super().form_valid(form)


def activate_user(request, token):
    user = User.objects.get(verification_token=token)
    user.verification_token = ''
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))
