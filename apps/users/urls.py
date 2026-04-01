from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView,
    UserProfileView,
    UserListView,
    RoleUpdateView,
    StatusUpdateView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('me/', UserProfileView.as_view(), name='profile'),
    
    # Admin endpoints
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/role/', RoleUpdateView.as_view(), name='role_update'),
    path('<int:pk>/status/', StatusUpdateView.as_view(), name='status_update'),
]
