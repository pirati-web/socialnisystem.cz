from functools import reduce
from operator import or_

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from bitfield import BitField

from .entryform import entry_form_config


class StateOffice(models.Model):
    """
    Represents a state office, bureau. Examples are: Úřad práce, OSSZ
    """
    name = models.CharField('Název', max_length=255)
    short_name = models.CharField('Zkratka názvu', max_length=50, help_text='např. OSSZ')

    class Meta:
        app_label = 'core'
        verbose_name = 'Úřad'
        verbose_name_plural = 'Úřady'

    def __str__(self):
        return self.short_name


class LifeConditionManager(models.Manager):
    def with_benefits(self):
        qset = self.get_queryset().prefetch_related('benefits__responsible_office')
        return ((lc, lc.benefits.all()) for lc in qset)


class LifeCondition(models.Model):
    """
    Represents a life condition of a benefit applicant. Used primarily for
    categorization.
    """
    title = models.CharField('Název', max_length=255)
    description = models.TextField('Popis', blank=True)

    objects = LifeConditionManager()

    class Meta:
        app_label = 'core'
        verbose_name = 'Źivotní situace'
        verbose_name_plural = 'Životní situace'
        ordering = ('title',)

    def __str__(self):
        return self.title


class BenefitAttachment(models.Model):
    """
    File attachments storage for benefits.
    """
    title = models.CharField('Titulek', max_length=255)
    file = models.FileField('Soubor')

    class Meta:
        app_label = 'core'
        verbose_name = 'Příloha k popisu dávky'
        verbose_name_plural = 'Přílohy k popisu dávky'

    def __str__(self):
        return self.title


class BenefitManager(models.Manager):
    def find_claimable(self, flags):
        """
        Searches `Benefit` objects whose requirements are satisfied by
        provided flag selection.

        Individual benefits can have multiple `BenefitRequirements` records.
        Benefit is only matched, if provided flags satisfy all the related
        `BenefitRequirement` records.

        `BenefitRequirement` is considered to be satisfied if any of the flags
        on `BenefitRequirement` record is  present in the provided flags.
        """
        query = reduce(or_, (models.Q(flags=f) for f in flags), models.Q())
        # Select all requirements that were not matched
        non_matched_requirements = BenefitRequirement.objects.exclude(query)
        # Select all benefits except those which have some unmatched requirement
        return self.get_queryset().exclude(requirements__pk__in=models.Subquery(non_matched_requirements.values('pk')))


class Benefit(models.Model):
    """
    A benefit from state social system.
    """
    name = models.CharField('Název', max_length=255)
    related_law = models.CharField('Související zákon(y)', max_length=255)

    base_description = models.TextField('Základní popis', blank=False)
    claim_description = models.TextField('Kdo má nárok', blank=False)
    other_description = models.TextField('Další informace', blank=True)

    responsible_office = models.ForeignKey(to='core.StateOffice', on_delete=models.PROTECT, verbose_name='Žádost se podává na')
    condition = models.ForeignKey(to='core.LifeCondition', related_name='benefits', on_delete=models.PROTECT, verbose_name='Situace')
    attachments = models.ManyToManyField(to='core.BenefitAttachment', blank=True, related_name='benefits')

    objects = BenefitManager()

    class Meta:
        app_label = 'core'
        verbose_name = 'Dávka'
        verbose_name_plural = 'Dávky'
        ordering = ('condition', 'name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('core:benefit-detail', kwargs={'pk': self.pk, 'slug': slugify(self.name)})


class BenefitRequirement(models.Model):
    # Individual requirements are represented as binary number instead of bunch of
    # boolean properties. This has several advantages:
    # - saves space in DB
    # - makes requirements easier to manage, code is cleaner
    benefit = models.ForeignKey(to='core.Benefit', on_delete=models.CASCADE, verbose_name='Dávka', related_name='requirements')
    flags = BitField(
        flags=entry_form_config.get_bitfield_flags(),
        verbose_name='Požadavky',
        help_text='Požadavky v rámci jednoho záznamu mají logický význam NEBO. '
                  'Dohoromady jsou pak spojeny logickou podmínkou A ZÁROVEŇ.',
        default=0
    )

    class Meta:
        app_label = 'core'
        verbose_name = 'Požadavek na získání dávky'
        verbose_name_plural = 'Požadavky na získání dávky'

    def __str__(self):
        return 'Sada požadavků dávky %s' % self.benefit
