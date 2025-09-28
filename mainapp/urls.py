from django.urls import path
from django.views.generic.base import RedirectView
from .views import UserFormView, PostFormView, DashboardView, login_view, logout_view, toggle_like, DetailedPostView, get_all_post_json, get_post_json

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("post/", RedirectView.as_view(url="/")),
    path("post/<int:pk>/like/", toggle_like, name="post_like"),
    path("post/<int:pk>", DetailedPostView.as_view(), name="detailed_post"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("signup", UserFormView.as_view()),
    
    path("api/posts", get_all_post_json, name="all_post"),
    path("api/posts/<int:post_id>", get_post_json, name="post_detailed")
]