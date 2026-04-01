import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

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

# ──────────────────────────────────────────────
# Registration Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestRegistration:
    def test_register_success(self, api_client):
        data = {
            'email': 'new@test.com', 'username': 'newuser',
            'password': 'StrongPass123!',
            'first_name': 'New', 'last_name': 'User'
        }
        response = api_client.post('/api/users/register/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(email='new@test.com')
        assert user.role == 'viewer'  # default role

    def test_register_weak_password(self, api_client):
        data = {
            'email': 'weak@test.com', 'username': 'weakuser',
            'password': '123',
            'first_name': 'Weak', 'last_name': 'User'
        }
        response = api_client.post('/api/users/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_email(self, api_client, viewer_user):
        data = {
            'email': 'viewer@test.com', 'username': 'another',
            'password': 'StrongPass123!',
            'first_name': 'Dup', 'last_name': 'User'
        }
        response = api_client.post('/api/users/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

# ──────────────────────────────────────────────
# Authentication Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestAuthentication:
    def test_login_success(self, api_client, viewer_user):
        response = api_client.post('/api/users/login/', {
            'email': 'viewer@test.com', 'password': 'ViewerPass123!'
        }, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_wrong_password(self, api_client, viewer_user):
        response = api_client.post('/api/users/login/', {
            'email': 'viewer@test.com', 'password': 'WrongPassword!'
        }, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

# ──────────────────────────────────────────────
# Profile & User Management Tests
# ──────────────────────────────────────────────

@pytest.mark.django_db
class TestUserManagement:
    def test_get_profile(self, api_client, viewer_user):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'viewer@test.com'
        assert response.data['role'] == 'viewer'

    def test_admin_can_list_users(self, api_client, admin_user, viewer_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_viewer_cannot_list_users(self, api_client, viewer_user):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.get('/api/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_change_role(self, api_client, admin_user, viewer_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(
            f'/api/users/{viewer_user.id}/role/',
            {'role': 'analyst'}, format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        viewer_user.refresh_from_db()
        assert viewer_user.role == 'analyst'

    def test_viewer_cannot_change_role(self, api_client, viewer_user, analyst_user):
        api_client.force_authenticate(user=viewer_user)
        response = api_client.patch(
            f'/api/users/{analyst_user.id}/role/',
            {'role': 'admin'}, format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_deactivate_user(self, api_client, admin_user, viewer_user):
        api_client.force_authenticate(user=admin_user)
        response = api_client.patch(
            f'/api/users/{viewer_user.id}/status/',
            {'is_active': False}, format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        viewer_user.refresh_from_db()
        assert viewer_user.is_active == False
