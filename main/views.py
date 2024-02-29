import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView, CreateView

from main.forms import DiagnosticForm, DiagnosticCategoryForm
from main.models import Diagnostic, DiagnosticCategory, TestCategory
from promo.models import Promo


class IndexView(generic.View):

    @staticmethod
    def get(request):
        three_promo = []

        # Выбираем три случайные акции (без повторов)
        all_active_promo = Promo.objects.filter(is_active=True)
        num_of_active_promo = all_active_promo.count()
        while len(three_promo) < 3:
            i = random.randint(0, num_of_active_promo - 1)
            if all_active_promo[i] not in three_promo:
                three_promo.append(all_active_promo[i])

        # for i in range(num_of_active_promo):
        #     three_promo.append(all_active_promo[i])

        context = {
            # 'count_users': 1,
            # 'count_schedules': 2,
            # 'count_active_schedules': 3,
            # 'count_unique_addresses': 4,
            'object_list': three_promo,
            # 'object_list': all_active_promo,
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
