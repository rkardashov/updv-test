from django.urls import path

from api.views import (
    SignUpView,
    SignInView,
    LogoutView,
    InfoView,
    LatencyView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('info/', InfoView.as_view(), name='info'),
    path('latency/', LatencyView.as_view(), name='latency'),
]
