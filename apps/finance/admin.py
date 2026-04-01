from django.contrib import admin
from .models import FinancialRecord

@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    list_display = ('category', 'type', 'amount', 'date', 'user', 'is_deleted')
    list_filter = ('type', 'category', 'is_deleted')
    search_fields = ('category', 'description')
    date_hierarchy = 'date'
    ordering = ('-date',)
