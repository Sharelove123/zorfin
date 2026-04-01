from django_filters import rest_framework as filters
from .models import FinancialRecord

class FinancialRecordFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')
    
    # Exact matches for category and type
    category = filters.CharFilter(lookup_expr='iexact')
    type = filters.ChoiceFilter(choices=FinancialRecord.RECORD_TYPES)

    class Meta:
        model = FinancialRecord
        fields = ['type', 'category', 'min_amount', 'max_amount', 'start_date', 'end_date']
