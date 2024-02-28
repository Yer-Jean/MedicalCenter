from django.shortcuts import render
from django.views import generic


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