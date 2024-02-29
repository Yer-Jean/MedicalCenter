from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse
from pytils.translit import slugify

from promo.forms import PromoForm
from promo.models import Promo


class PromoListView(ListView):
    model = Promo


class PromoCreateView(LoginRequiredMixin, CreateView):
    model = Promo
    form_class = PromoForm

    def get_success_url(self):
        return reverse('promo:promos')
        # return reverse('promo:promo_view', args=[self.object.slug])

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.title)
            self.object.save()

        return super().form_valid(form)
