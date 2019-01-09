from django.urls import include, path
from .views import UserCreateApiView, LoginApiView

urlpatterns = [
    path('signup/', UserCreateApiView.as_view()),
    path('login/', LoginApiView.as_view()),
]