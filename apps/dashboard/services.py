from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from apps.finance.models import FinancialRecord
from decimal import Decimal

class DashboardService:
    @staticmethod
    def _base_queryset():
        return FinancialRecord.objects.filter(is_deleted=False)

    @staticmethod
    def get_summary():
        qs = DashboardService._base_queryset()
        income = qs.filter(type='income').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        expenses = qs.filter(type='expense').aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        return {
            "total_income": income,
            "total_expenses": expenses,
            "net_balance": income - expenses
        }

    @staticmethod
    def get_category_breakdown():
        qs = DashboardService._base_queryset()
        return list(
            qs.values('category', 'type')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

    @staticmethod
    def get_monthly_trends():
        qs = DashboardService._base_queryset()
        
        trends = (
            qs.annotate(month=TruncMonth('date'))
            .values('month', 'type')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        
        # Formatting the response for easy frontend use
        formatted_trends = {}
        for item in trends:
            month_str = item['month'].strftime('%Y-%m')
            
            if month_str not in formatted_trends:
                formatted_trends[month_str] = {"income": Decimal('0.00'), "expense": Decimal('0.00')}
                
            formatted_trends[month_str][item['type']] = item['total']
            
        return [
            {"month": k, "income": v["income"], "expense": v["expense"]} 
            for k, v in formatted_trends.items()
        ]

    @staticmethod
    def get_recent_activity(limit=10):
        # We can leverage the serializer from finance app, 
        # or simply return the ORM dicts here. We'll return the queryset 
        # and let the View serialize it for maximum flexibility.
        return DashboardService._base_queryset()[:limit]
