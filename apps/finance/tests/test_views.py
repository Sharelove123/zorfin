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
            category='Salary', date=date(2026, 1, 15), description='Monthly salary'
        ),
        FinancialRecord.objects.create(
            user=admin_user, amount=Decimal('1200.00'), type='expense',
            category='Rent', date=date(2026, 1, 20), description='Office rent'
        ),
        FinancialRecord.objects.create(
            user=admin_user, amount=Decimal('300.00'), type='expense',
            category='Utilities', date=date(2026, 2, 5), description='Electric bill'
        ),
    ]
    return records

# ──────────────────────────────────────────────
# CRUD Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestFinancialRecordCRUD:
    def test_admin_can_create_record(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'amount': '2500.00', 'type': 'income',
            'category': 'Freelance', 'date': '2026-03-10',
            'description': 'Client project payment'
        }
        response = api_client.post('/api/finance/records/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['amount'] == '2500.00'
        assert response.data['user'] == admin_user.id

    def test_viewer_cannot_create_record(self, api_client, viewer_user):
        api_client.force_authenticate(user=viewer_user)
        data = {
            'amount': '100.00', 'type': 'expense',
            'category': 'Food', 'date': '2026-03-10'
        }
        response = api_client.post('/api/finance/records/', data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewer_can_list_records(self, api_client, viewer_user, sample_records):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/finance/records/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_admin_can_update_record(self, api_client, admin_user, sample_records):
        api_client.force_authenticate(user=admin_user)
        record = sample_records[0]
        response = api_client.patch(
            f'/api/finance/records/{record.id}/',
            {'amount': '5500.00'}, format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        record.refresh_from_db()
        assert record.amount == Decimal('5500.00')

    def test_soft_delete(self, api_client, admin_user, sample_records):
        api_client.force_authenticate(user=admin_user)
        record = sample_records[0]
        response = api_client.delete(f'/api/finance/records/{record.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        record.refresh_from_db()
        assert record.is_deleted == True
        # Verify it no longer appears in GET list
        response = api_client.get('/api/finance/records/')
        assert len(response.data['results']) == 2

    def test_invalid_amount_rejected(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'amount': '-50.00', 'type': 'expense',
            'category': 'Food', 'date': '2026-03-10'
        }
        response = api_client.post('/api/finance/records/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

# ──────────────────────────────────────────────
# Filtering Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestFinancialRecordFiltering:
    def test_filter_by_type(self, api_client, admin_user, sample_records):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/finance/records/?type=income')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['type'] == 'income'

    def test_filter_by_category(self, api_client, admin_user, sample_records):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/finance/records/?category=rent')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_filter_by_date_range(self, api_client, admin_user, sample_records):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/finance/records/?start_date=2026-02-01&end_date=2026-02-28')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_filter_by_amount_range(self, api_client, admin_user, sample_records):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/finance/records/?min_amount=1000&max_amount=6000')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
