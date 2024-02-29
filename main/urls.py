from django.urls import path

from main.apps import MainConfig
from main.views import *

app_name = MainConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('diagnostics/', DiagnosticCategoryListView.as_view(), name='diagnostics'),
    path('diagnostics/category_create/', DiagnosticCategoryCreateView.as_view(), name='diagnostic_category_create'),
    path('diagnostics/create/', DiagnosticCreateView.as_view(), name='diagnostic_create'),

    path('tests/', TestCategoryListView.as_view(), name='tests'),
]