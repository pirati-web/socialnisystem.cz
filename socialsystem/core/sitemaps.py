from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Benefit


class BenefitSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Benefit.objects.all()


class StaticViewSitemap(Sitemap):
    priority = 1
    changefreq = 'monthly'

    def items(self):
        return ['core:benefit-overview', 'core:benefit-claim']

    def location(self, item):
        return reverse(item)



sitemaps = {
    'core:benefits': BenefitSitemap,
    'core:views': StaticViewSitemap,
}
