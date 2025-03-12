from django.contrib import admin
from django.urls import path, include, re_path
from users import urls as users_urls
from users import views as users_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include('djoser.urls.authtoken')),
    path("api/", include(users_urls)),
    path('api/auth/activate/<uid>/<token>/', users_views.UserActivationView.as_view(), name='user-activate'),
]
