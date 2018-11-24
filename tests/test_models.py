import pytest

from django.conf import settings

from socialsystem.core.models import Benefit, BenefitRequirement, StateOffice, LifeCondition
from socialsystem.core.entryform import entry_form_config


def prepare_benefits_with_requirements():
    lifeconditions = [
        {
            'id': 1,
            'title': 'A life condition',
        }
    ]

    state_offices = [
        {
            'id': 1,
            'name': 'State office',
            'short_name': 'SO',
        }
    ]

    benefits = [
        {
            'id': 1,
            'name': 'Benefit1',
            'related_law': 'A law',
            'base_description': '...',
            'usecase_description': '...',
            'claim_description': '...',
            'other_description': '...',
        },
        {
            'id': 2,
            'name': 'Benefit2',
            'related_law': 'A law',
            'base_description': '...',
            'usecase_description': '...',
            'claim_description': '...',
            'other_description': '...',
        },
        {
            'id': 3,
            'name': 'Benefit3',
            'related_law': 'A law',
            'base_description': '...',
            'usecase_description': '...',
            'claim_description': '...',
            'other_description': '...',
        }
    ]

    benefit_requirements = [
        {
            'flags': BenefitRequirement.flags.bit_5 | BenefitRequirement.flags.bit_6
        },
        {
            'flags': BenefitRequirement.flags.bit_13
        },
        {
            'flags': BenefitRequirement.flags.bit_21 | BenefitRequirement.flags.bit_5
        },
    ]

    lifecondition1 = LifeCondition.objects.create(**lifeconditions[0])
    state_office1 = StateOffice.objects.create(**state_offices[0])
    benefit1 = Benefit.objects.create(condition=lifecondition1, responsible_office=state_office1, **benefits[0])
    benefit2 = Benefit.objects.create(condition=lifecondition1, responsible_office=state_office1, **benefits[1])
    benefit3 = Benefit.objects.create(condition=lifecondition1, responsible_office=state_office1, **benefits[2])

    # benefit1 requires either bit_5 OR bit_6
    BenefitRequirement.objects.create(benefit=benefit1, **benefit_requirements[0])

    # benefit2 requires (bit_5 OR bit_6) AND bit_13
    BenefitRequirement.objects.create(benefit=benefit2, **benefit_requirements[0])
    BenefitRequirement.objects.create(benefit=benefit2, **benefit_requirements[1])

    # benefit3 requires (bit_5 OR bit_6) AND bit_13 AND (bit_21 OR bit_5)
    BenefitRequirement.objects.create(benefit=benefit3, **benefit_requirements[0])
    BenefitRequirement.objects.create(benefit=benefit3, **benefit_requirements[1])
    BenefitRequirement.objects.create(benefit=benefit3, **benefit_requirements[2])


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize(
    'flags, expected',
    (
        ((), []),
        (
            (BenefitRequirement.flags.bit_17,),
            []
        ),
        (
            (BenefitRequirement.flags.bit_5,),
            ['Benefit1',]
        ),
        (
            (BenefitRequirement.flags.bit_6,),
            ['Benefit1',]
        ),
        (
            (BenefitRequirement.flags.bit_6, BenefitRequirement.flags.bit_5,),
            ['Benefit1',]
        ),
        (
            (BenefitRequirement.flags.bit_6, BenefitRequirement.flags.bit_17,),
            ['Benefit1',]
        ),
        (
            (BenefitRequirement.flags.bit_6, BenefitRequirement.flags.bit_13,),
            ['Benefit1', 'Benefit2',]
        ),
        (
            (BenefitRequirement.flags.bit_6, BenefitRequirement.flags.bit_13, BenefitRequirement.flags.bit_21),
            ['Benefit1', 'Benefit2', 'Benefit3',]
        ),
        (
            (BenefitRequirement.flags.bit_5, BenefitRequirement.flags.bit_13, BenefitRequirement.flags.bit_21),
            ['Benefit1', 'Benefit2', 'Benefit3',]
        ),
    ),
)
def test_benefit__find_by_satisfied_requirements(flags, expected):
    prepare_benefits_with_requirements()
    benefit_names = Benefit.objects.find_claimable(flags).values_list('name', flat=True)
    assert list(benefit_names) == expected
