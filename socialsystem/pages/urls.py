from django.contrib.flatpages.views import flatpage
from django.urls import path
from django.views.generic.base import RedirectView

app_name = 'pages'

urlpatterns = [
    path('kalkulacka', RedirectView.as_view(url='/nase-reseni/rodicovsky-prispevek/')),
    path('<path:url>', flatpage),
]
