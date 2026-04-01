from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.users.permissions import IsAnalystOrAdmin
from apps.finance.serializers import FinancialRecordListSerializer
from .services import DashboardService


class DashboardSummaryView(APIView):
    """
    Returns total income, total expenses, and net balance.
    Access: Analyst and Admin.
    """
    permission_classes = [permissions.IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        data = DashboardService.get_summary()
        return Response(data)


class DashboardCategoryBreakdownView(APIView):
    """
    Returns totals grouped by category.
    Access: Analyst and Admin.
    """
    permission_classes = [permissions.IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        data = DashboardService.get_category_breakdown()
        return Response(data)


class DashboardMonthlyTrendsView(APIView):
    """
    Returns total income and expenses grouped by month.
    Access: Analyst and Admin.
    """
    permission_classes = [permissions.IsAuthenticated, IsAnalystOrAdmin]

    def get(self, request):
        data = DashboardService.get_monthly_trends()
        return Response(data)


class DashboardRecentActivityView(APIView):
    """
    Returns the 10 most recent financial records.
    Access: All authenticated roles (Viewer, Analyst, Admin).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = DashboardService.get_recent_activity(limit=10)
        serializer = FinancialRecordListSerializer(queryset, many=True)
        return Response(serializer.data)
