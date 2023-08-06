from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        "^get_paddle_info/$", views.get_paddle_info, name="get_paddle_info"
    ),
    re_path(
        "^get_subscription_details/$",
        views.get_subscription_details,
        name="get_subscription_details",
    ),
    re_path("webhook/$", views.webhook, name="webhook"),
]
