from django.contrib import admin
from django.db.models import TextField

from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from markdownx.widgets import AdminMarkdownxWidget

from . import models


@admin.register(models.StateOffice)
class StateOfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')


@admin.register(models.LifeCondition)
class LifeConditionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BenefitAttachment)
class BenefitAttachmentAdmin(admin.ModelAdmin):
    pass


class BenefitAttachmentInline(admin.TabularInline):
    model = models.Benefit.attachments.through
    extra = 1
    verbose_name = 'Příloha'
    verbose_name_plural = 'Přílohy'


class BenefitRequirementInline(admin.StackedInline):
    model = models.BenefitRequirement
    extra = 0
    verbose_name = 'Požadavek'
    verbose_name_plural = 'Požadavky'

    formfield_overrides = {
        BitField: {'widget': BitFieldCheckboxSelectMultiple},
    }


@admin.register(models.Benefit)
class BenefitAdmin(admin.ModelAdmin):
    exclude = ('attachments',)
    list_display = ('name', 'condition', 'responsible_office', 'searchable')
    list_select_related = ('condition', 'responsible_office')
    list_filter = ('condition', 'responsible_office', 'searchable')

    inlines = [
        BenefitRequirementInline,
        BenefitAttachmentInline,
    ]

    formfield_overrides = {
        TextField: {'widget': AdminMarkdownxWidget},
    }



