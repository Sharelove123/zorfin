import pytest
from decimal import Decimal
from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.finance.models import FinancialRecord

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email='admin@test.com', username='admin', password='AdminPass123!',
        first_name='Admin', last_name='User', role='admin'
    )

@pytest.fixture
def analyst_user(db):
    return User.objects.create_user(
        email='analyst@test.com', username='analyst', password='AnalystPass123!',
        first_name='Analyst', last_name='User', role='analyst'
    )

@pytest.fixture
def viewer_user(db):
    return User.objects.create_user(
        email='viewer@test.com', username='viewer', password='ViewerPass123!',
        first_name='Viewer', last_name='User', role='viewer'
    )

@pytest.fixture
def sample_records(admin_user):
    records = [
        FinancialRecord.objects.create(
            user=admin_user, amount=Decimal('5000.00'), type='income',
            category='Salary', date=date(2026, 1, 15)
        ),
        FinancialRecord.objects.create(
            user=admin_user, amount=Decimal('3000.00'), type='income',
            category='Freelance', date=date(2026, 2, 10)
        ),
        FinancialRecord.objects.create(
            user=admin_user, amount=Decimal('1200.00'), type='expense',
            category='Rent', date=date(2026, 1, 20)
        ),
        FinancialRecord.objects.create(
            user=admin_user, amount=Decimal('300.00'), type='expense',
            category='Utilities', date=date(2026, 2, 5)
        ),
    ]
    return records

# ──────────────────────────────────────────────
# Dashboard Summary Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestDashboardSummary:
    def test_analyst_can_access_summary(self, api_client, analyst_user, sample_records):
        api_client.force_authenticate(user=analyst_user)
        response = api_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_200_OK
        assert Decimal(str(response.data['total_income'])) == Decimal('8000.00')
        assert Decimal(str(response.data['total_expenses'])) == Decimal('1500.00')
        assert Decimal(str(response.data['net_balance'])) == Decimal('6500.00')

    def test_viewer_cannot_access_summary(self, api_client, viewer_user, sample_records):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_access_summary(self, api_client, admin_user, sample_records):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_200_OK

# ──────────────────────────────────────────────
# Dashboard Category Breakdown Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestDashboardCategories:
    def test_analyst_can_access_categories(self, api_client, analyst_user, sample_records):
        api_client.force_authenticate(user=analyst_user)
        response = api_client.get('/api/dashboard/categories/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4  # Salary-income, Freelance-income, Rent-expense, Utilities-expense

    def test_viewer_cannot_access_categories(self, api_client, viewer_user, sample_records):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/dashboard/categories/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

# ──────────────────────────────────────────────
# Dashboard Monthly Trends Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestDashboardTrends:
    def test_analyst_can_access_trends(self, api_client, analyst_user, sample_records):
        api_client.force_authenticate(user=analyst_user)
        response = api_client.get('/api/dashboard/trends/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # January and February

    def test_viewer_cannot_access_trends(self, api_client, viewer_user, sample_records):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/dashboard/trends/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

# ──────────────────────────────────────────────
# Dashboard Recent Activity Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestDashboardRecent:
    def test_viewer_can_access_recent(self, api_client, viewer_user, sample_records):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/dashboard/recent/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_unauthenticated_cannot_access(self, api_client, sample_records):
        response = api_client.get('/api/dashboard/recent/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
