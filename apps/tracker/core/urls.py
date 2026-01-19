from django.urls import path, include

import core.views as views


urlpatterns = [
    path("announce/", views.announce, name="announce"),
]
