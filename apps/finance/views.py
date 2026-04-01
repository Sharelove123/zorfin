from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count

from .models import FinancialRecord
from .serializers import FinancialRecordSerializer, FinancialRecordListSerializer
from .filters import FinancialRecordFilter
from .permissions import IsAdminOrReadOnly


class FinancialRecordViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for financial records. 
    Admins can create/update/delete.
    Viewers and Analysts can only list/retrieve.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    filterset_class = FinancialRecordFilter
    search_fields = ['description', 'category']
    ordering_fields = ['date', 'amount', 'created_at']

    def get_queryset(self):
        # Exclude soft-deleted records for typical operations
        return FinancialRecord.objects.filter(is_deleted=False)

    def get_serializer_class(self):
        if self.action in ['list']:
            return FinancialRecordListSerializer
        return FinancialRecordSerializer

    def perform_create(self, serializer):
        # Admin is automatically set as the creator
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.save()


class CategoryListView(APIView):
    """
    Returns a list of all distinct categories that have been used, along with their usage count.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        categories = (
            FinancialRecord.objects.filter(is_deleted=False)
            .values('category')
            .annotate(count=Count('category'))
            .order_by('-count')
        )
        return Response(categories, status=status.HTTP_200_OK)
