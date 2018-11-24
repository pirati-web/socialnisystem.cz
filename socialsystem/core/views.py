from django.views.generic import TemplateView, FormView

from .entryform import EntryForm, entry_form_config
from .models import LifeCondition


class BenefitOverview(TemplateView):
    template_name = 'core/benefit_overview.html'

    def get_context_data(self):
        data = super().get_context_data()
        data['life_conditions'] = LifeCondition.objects.with_benefits()
        return data


class BenefitClaimView(FormView):
    template_name = 'core/benefit_claim.html'
    form_class = EntryForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs['entry_form_config'] = entry_form_config
        return kwargs
