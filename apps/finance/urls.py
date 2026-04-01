from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FinancialRecordViewSet, CategoryListView

router = DefaultRouter()
router.register(r'records', FinancialRecordViewSet, basename='records')

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('', include(router.urls)),
]
