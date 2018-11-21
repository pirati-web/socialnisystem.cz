from django.contrib import admin
from django.db.models import TextField

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


@admin.register(models.Benefit)
class BenefitAdmin(admin.ModelAdmin):
    exclude = ('attachments',)
    list_display = ('name', 'condition', 'related_law', 'responsible_office')
    list_select_related = ('condition', 'responsible_office')
    list_filter = ('condition', 'responsible_office')

    inlines = [
        BenefitAttachmentInline,
    ]

    formfield_overrides = {
        TextField: {'widget': AdminMarkdownxWidget},
    }



