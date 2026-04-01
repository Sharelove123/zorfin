from django.db import models
from django.conf import settings

class FinancialRecord(models.Model):
    RECORD_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='financial_records'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=RECORD_TYPES)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
        
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.type.capitalize()} - {self.category}: {self.amount} on {self.date}"

    # Soft delete override
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
