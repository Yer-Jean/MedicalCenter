from django import forms

from main.models import Diagnostic, DiagnosticCategory
from users.forms import StyleFormMixin


class DiagnosticCategoryForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = DiagnosticCategory
        exclude = ('created_by',)


class DiagnosticForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Diagnostic
        exclude = ('created_by',)
