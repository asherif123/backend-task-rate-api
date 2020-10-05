from django.urls import include, path
from rest_framework import routers

from exchangerates import views

router = routers.DefaultRouter()
router.register(r'rates', views.RateViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
]
