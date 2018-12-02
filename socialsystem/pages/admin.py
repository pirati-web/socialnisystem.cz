from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db.models import TextField

from markdownx.widgets import AdminMarkdownxWidget

from .models import FlatPageMeta


class MetadataInline(admin.StackedInline):
    model = FlatPageMeta


class MarkdownFlatPageAdmin(FlatPageAdmin):
    inlines = (MetadataInline,)
    formfield_overrides = {
        TextField: {'widget': AdminMarkdownxWidget},
    }



admin.site.unregister(FlatPage)
admin.site.register(FlatPage, MarkdownFlatPageAdmin)
