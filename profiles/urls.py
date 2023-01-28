from django.urls import path, include
from . import views

urlpatterns = [
    path("<int:user_id>/<str:username>", views.profile, name="profile"),
]
