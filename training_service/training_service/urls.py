from django.contrib import admin
from django.urls import path, include
from trainings.urls import urlpatterns as trainings_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(trainings_urls)),
]
