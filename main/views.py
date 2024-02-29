from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import ListView, CreateView

from main.forms import DiagnosticForm, DiagnosticCategoryForm
from main.models import Diagnostic, DiagnosticCategory, TestCategory


class IndexView(generic.View):

    @staticmethod
    def get(request):
        context = {
            'count_users': 1,
            'count_schedules': 2,
            'count_active_schedules': 3,
            'count_unique_addresses': 4,
            # 'object_list': three_random_articles,
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
