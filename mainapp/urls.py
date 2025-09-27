from django.urls import path
from django.views.generic.base import RedirectView
from .views import UserFormView, PostFormView, DashboardView, login_view, logout_view, toggle_like, DetailedPostView, map_view

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("post/", RedirectView.as_view(url="/")),
    path("post/<int:pk>/like/", toggle_like, name="post-like"),
    path("post/<int:pk>", DetailedPostView.as_view(), name="detailed_post"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("signup", UserFormView.as_view()),
    
    path("map_view", map_view, name="map_view")
]