from django.urls import path

from .views import (
    DashboardSummaryView,
    DashboardCategoryBreakdownView,
    DashboardMonthlyTrendsView,
    DashboardRecentActivityView
)

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard_summary'),
    path('categories/', DashboardCategoryBreakdownView.as_view(), name='dashboard_categories'),
    path('trends/', DashboardMonthlyTrendsView.as_view(), name='dashboard_trends'),
    path('recent/', DashboardRecentActivityView.as_view(), name='dashboard_recent'),
]
