from django.contrib import admin
from django.urls import path, include, re_path
from users import urls as users_urls
from users import views as users_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Users Service API",
      default_version='v1',
      description="API of users service",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="dibilarts@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include('djoser.urls.authtoken')),
    path("api/", include(users_urls)),
    path('api/auth/activate/<uid>/<token>/', users_views.UserActivationView.as_view(), name='user-activate'),
    path('api/auth/o/', include('allauth.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('django_prometheus.urls')),
]