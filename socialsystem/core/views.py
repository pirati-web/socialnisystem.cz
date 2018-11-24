from django.views.generic import TemplateView, FormView
from django.urls import reverse

from .entryform import EntryForm, entry_form_config, build_question_flag
from .models import LifeCondition, Benefit, BenefitRequirement


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

    def form_valid(self, form):
        selected_flags = []

        # Assemble query
        for question in entry_form_config:
            flag = form.cleaned_data.get(str(question['id']), False)

            if flag:
                selected_flags.append(getattr(BenefitRequirement.flags, build_question_flag(question)))

        return self.render_to_response({
            'form': form,
            'submitted': True,
            'claimable_benefits': Benefit.objects.find_claimable(selected_flags),
        })
