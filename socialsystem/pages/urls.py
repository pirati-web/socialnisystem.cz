from django.contrib.flatpages.views import flatpage
from django.urls import path, re_path
from django.views.generic.base import RedirectView

app_name = 'pages'

urlpatterns = [
    re_path('kalkulacka/?', RedirectView.as_view(url='/nase-reseni/rodicovsky-prispevek/', permanent=False)),
    path('<path:url>', flatpage),
]
