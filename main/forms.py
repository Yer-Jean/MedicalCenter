from django import forms

from main.models import Diagnostic, DiagnosticCategory, MedicalResult
from users.forms import StyleFormMixin
from users.models import User


class DiagnosticCategoryForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = DiagnosticCategory
        exclude = ('created_by',)


class DiagnosticForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Diagnostic
        exclude = ('created_by',)


class MedicalResultForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MedicalResult
        exclude = ('doctor',)
        # widgets = {
        #     'user': forms.Select(attrs={'class': 'form-control'}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #  Передаем в форму список пользователей из get_user_queryset
        self.fields['user'].queryset = self.get_user_queryset()
        # Выводим этот список в виде 'Имя Фамилия' не трогая метод str() модели User
        self.fields['user'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    def get_user_queryset(self):
        # Выбираем только тех пользователей, которые не входят ни в какую
        # группу (doctors, managers), то есть обычных пользователей/пациентов
        return User.objects.filter(groups__isnull=True)


class MedicalResultFileForm(StyleFormMixin, forms.Form):
    file = forms.FileField(label='Загрузить файл', required=False)
    file_description = forms.CharField(label='Описание файла', max_length=50, required=False)
    # delete_file = forms.BooleanField(label='Удалить файл', required=False)
