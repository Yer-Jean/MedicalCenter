from django.urls import path

from promo.apps import PromoConfig
from promo.views import *

app_name = PromoConfig.name

urlpatterns = [
    path('', PromoListView.as_view(), name='promos'),

    path('create/', PromoCreateView.as_view(), name='promo_create'),
]
