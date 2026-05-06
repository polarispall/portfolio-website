from django.urls import path
from .views import PortfolioView, ProjectDetailView

app_name = 'core'

urlpatterns = [
    path('', PortfolioView.as_view(), name='portfolio'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]
