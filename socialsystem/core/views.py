from django.views.generic import TemplateView

from .models import LifeCondition


class BenefitOverview(TemplateView):
    template_name = 'core/benefit_overview.html'

    def get_context_data(self):
        data = super().get_context_data()
        data['life_conditions'] = LifeCondition.objects.with_benefits()
        return data
