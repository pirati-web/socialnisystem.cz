from django.views.generic import TemplateView, DetailView
from django.urls import path

from . import models
from . import views


app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/home.html')),
    path('davky/<int:pk>-<str:slug>/', DetailView.as_view(model=models.Benefit, template_name='core/benefit_detail.html'), name='benefit-detail'),
    path('davky/prehled/', views.BenefitOverview.as_view(), name='benefit-overview'),
    path('davky/na-co-mam-narok/', views.BenefitClaimView.as_view(), name='benefit-claim'),
]
