from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from doctors.forms import DoctorEditForm
from doctors.models import Doctor
from users.forms import LoginForm, UserRegisterForm, UserForm
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


class UserDetailView(LoginRequiredMixin, DetailView):
    # Отсутствует модель, так как get_queryset вернет динамически модель,
    # в зависимости от группы, в которую входит пользователь
    # model = User

    def get_form_class(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Определяем класс формы в зависимости от роли пользователя
        if user.groups.filter(name='doctors').exists():
            return DoctorEditForm  # Кастомная форма для доктора
        # elif user.groups.filter(name='managers').exists():
        #     return ModeratorEditForm  # Кастомная форма для модератора
        else:
            return None  # Возвращаем None для использования формы по умолчанию

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем форму
        form_class = self.get_form_class()
        if form_class:
            form = form_class(instance=self.object)
            context['form'] = form

        return context

    def get_queryset(self):
        # Получаем текущего пользователя
        user = self.request.user

        # Определяем модель в зависимости от роли пользователя
        if user.groups.filter(name='doctors').exists():
            return Doctor.objects.all()  # Возвращаем модель Doctor
        # elif user.groups.filter(name='managers').exists():
        #     return Managers.objects.all()  # Возвращаем модель Manager
        else:
            return User.objects.all()  # Возвращаем модель User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm

    def get_success_url(self):
        return reverse('users:user_view', args=[self.kwargs.get('pk')])


def activate_user(request, token):
    user = User.objects.get(verification_token=token)
    user.verification_token = ''
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
