import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import ListView, CreateView, DetailView, FormView

from doctors.models import Doctor
from main.forms import DiagnosticForm, DiagnosticCategoryForm, MedicalResultForm, MedicalResultFileForm
from main.models import Diagnostic, DiagnosticCategory, TestCategory, MedicalResult, MedicalResultFile
from promo.models import Promo
from users.models import User


class IndexView(generic.View):

    @staticmethod
    def get(request):
        three_promo = []

        count_tests = MedicalResult.objects.all().count()
        count_doctors = Doctor.objects.all().count()
        # Считаем обычных пользователей (не входящих в группы doctors, managers, staff...)
        count_users = User.objects.filter(groups__isnull=True).count()

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

        context = {
            'count_tests': count_tests,
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


class ResultListView(LoginRequiredMixin, ListView):
    model = MedicalResult

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(doctor=self.request.user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medical_results = self.get_queryset()
        medical_result_files = {}
        for result in medical_results:
            try:
                medical_result_file = result.medicalresultfile
                if medical_result_file:
                    medical_result_files[result.id] = medical_result_file.file.url
            except MedicalResultFile.DoesNotExist:
                pass
        context['medical_result_files'] = medical_result_files
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     medical_results = self.get_queryset()
    #     medical_result_files = {}
    #     for result in medical_results:
    #         if result.medicalresultfile:
    #             medical_result_files[result.id] = result.medicalresultfile.file.url
    #             break  # Закончим цикл, если найден файл
    #     context['medical_result_files'] = medical_result_files
    #     return context


class ResultCreateView(FormView):
    model = MedicalResult
    form_class = MedicalResultForm
    file_form_class = MedicalResultFileForm
    template_name = 'main/medicalresult_form.html'

    def form_valid(self, form):
        # result_instance = form.save(commit=False)
        self.object = form.save(commit=False)  # Сначала сохраняем форму, но не в базу данных
        # Получаем объект врача, соответствующего текущему пользователю
        doctor = Doctor.objects.get(user=self.request.user)
        self.object.doctor = doctor  # Присваиваем врача записи MedicalResult
        self.object.save()  # Теперь сохраняем запись MedicalResult
        # result_instance.save()
        file_form = self.file_form_class(self.request.POST, self.request.FILES)
        if file_form.is_valid():
            file_description = file_form.cleaned_data['file_description']
            if 'file' in self.request.FILES:
                file_instance = MedicalResultFile(medical_result=self.object, file=self.request.FILES['file'], file_description=file_description)
                # file_instance = MedicalResultFile(medical_result=result_instance, file=self.request.FILES['file'])
                file_instance.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['file_form'] = self.file_form_class()
        return context

    def get_success_url(self):
        return reverse('main:results')
            # return reverse('main:result_view', args=[self.object.pk])


# class ResultCreateView(LoginRequiredMixin, CreateView):
#     model = MedicalResult
#     form_class = MedicalResultForm
#
#     def get_success_url(self):
#         return reverse('main:results')
#         # return reverse('main:result_view', args=[self.object.pk])
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)  # Сначала сохраняем форму, но не в базу данных
#         doctor = Doctor.objects.get(user=self.request.user)  # Получаем объект врача, соответствующего текущему пользователю
#         self.object.doctor = doctor  # Присваиваем врача записи MedicalResult
#         self.object.save()  # Теперь сохраняем запись MedicalResult
#         return super().form_valid(form)

class ResultDetailView(LoginRequiredMixin, DetailView):
    model = MedicalResult

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medical_result = self.get_object()
        if hasattr(medical_result, 'medicalresultfile'):
            context['medical_result_file'] = medical_result.medicalresultfile.file.url
            context['medical_result_file_description'] = medical_result.medicalresultfile.file_description
        else:
            context['medical_result_file'] = None

        return context
