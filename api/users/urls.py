from django.urls import include, path
from rest_framework import routers
# from .views import UserViewSet, UserProfileViewSet
from .views import UserList, UserDetail, UserCreate, UserUpdate, UserDelete, UpdatePassword, ProfileImageUpdate, CustomAuthToken

# router = routers.DefaultRouter()
# router.register(r'', UserViewSet)
# router.register(r'profiles', UserProfileViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
#     # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# ]

urlpatterns = [
    path(r'', UserList.as_view(), name='user-list'),
    path(r'/<int:pk>', UserDetail.as_view(), name='user-detail'),
    path(r'/register', UserCreate.as_view(), name='user-register'),
    path(r'/<int:pk>/update', UserUpdate.as_view(), name='user-update'),
    path(r'/<int:pk>/delete', UserDelete.as_view(), name='user-delete'),
    path(r'/new-password', UpdatePassword.as_view(), name='password-update'),
    path(r'/profile/<int:pk>/picture-upload', ProfileImageUpdate.as_view(), name='picture-upload'),

    path(r'/auth', CustomAuthToken.as_view(), name='user-auth'),
]