# charts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chart/<int:year>/<str:chart_type>/', views.chart_view, name='chart_view'),
    path('charts/mean_median/', views.create_chart_for_mean_and_meadian, name='create_chart_for_mean_and_meadian'),
]
