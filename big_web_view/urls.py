from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.views.decorators.cache import never_cache
from big_web_cam.views import profile, BwcLogoutView, BwcLoginView, ChangeUserInfoView, BwcPasswordChangeView, \
    RergisterUserView, RegisterDoneView, user_activate, DeleteUserView

urlpatterns = [
    path('', include('big_web_cam.ulrs')),
    path('admin/', admin.site.urls),
    path('accounts/profile/delete/', DeleteUserView.as_view() , name = 'profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view() , name = 'profile_change'),
    path('accounts/profile/', profile, name = 'profile'),
    path('accounts/logout/', BwcLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BwcPasswordChangeView.as_view() , name = 'password_change'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RergisterUserView.as_view(), name='register'),
    path('accounts/login/', BwcLoginView.as_view(), name='login'),
]
