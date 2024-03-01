import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView, CreateView

from doctors.models import Doctor
from main.forms import DiagnosticForm, DiagnosticCategoryForm
from main.models import Diagnostic, DiagnosticCategory, TestCategory
from promo.models import Promo
from users.models import User


class IndexView(generic.View):

    @staticmethod
    def get(request):
        three_promo = []
        # count_tests = User.objects.all().count()
        count_doctors = Doctor.objects.all().count()
        count_users = User.objects.all().count()
        # Выбираем три случайные акции (без повторов)
        all_active_promo = Promo.objects.filter(is_active=True)
        num_of_active_promo = all_active_promo.count()
        if num_of_active_promo <= 3:
            three_promo = all_active_promo
        else:
            while len(three_promo) < 3:
                i = random.randint(0, num_of_active_promo - 1)
                if all_active_promo[i] not in three_promo:
                    three_promo.append(all_active_promo[i])

# TODO заполнить численные данные из БД
        context = {
            'count_tests': 3,
            'count_doctors': count_doctors,
            'count_users': count_users,
            'object_list': three_promo,
        }
        return render(request, 'main/index.html', context)


class DiagnosticCategoryListView(ListView):
    model = DiagnosticCategory


class DiagnosticCategoryCreateView(LoginRequiredMixin, CreateView):
    model = DiagnosticCategory
    form_class = DiagnosticCategoryForm

    def get_success_url(self):
        return reverse('main:diagnostics', args=[self.object.pk])


class DiagnosticListView(ListView):
    model = Diagnostic


class DiagnosticCreateView(LoginRequiredMixin, CreateView):
    model = Diagnostic
    form_class = DiagnosticForm


class TestCategoryListView(ListView):
    model = TestCategory
