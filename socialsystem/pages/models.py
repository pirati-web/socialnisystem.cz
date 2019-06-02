from django.db import models


class FlatPageMeta(models.Model):
    flatpage = models.OneToOneField(to='flatpages.FlatPage', on_delete=models.CASCADE, verbose_name='Stránka', related_name='metadata')
    title = models.CharField('Titulek', max_length=255, blank=True)
    keywords = models.CharField('Klíčová slova', help_text='Oddělujte čárkou', max_length=150, blank=True)
    description = models.TextField('Krátký popis', blank=True)

    class Meta:
        verbose_name = 'Metadata statické stránky'
        verbose_name_plural = 'Metadata statických stránek'

    def __str__(self):
        return 'Metadata pro %s' % self.flatpage
