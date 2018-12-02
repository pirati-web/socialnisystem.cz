from django.contrib.flatpages.views import flatpage
from django.urls import path

app_name = 'pages'

urlpatterns = [
    path('<path:url>', flatpage),
]
