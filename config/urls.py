from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from optics.users.views import LoginView


urlpatterns = [
    path('', LoginView.as_view()),
    path('admin-portal/', admin.site.urls),
    path('users/', include("optics.users.urls"), ),
    path('submissions/', include("optics.submissions.urls"), ),
    path('dashboards/', include("optics.dashboards.urls"), ),
] + staticfiles_urlpatterns()
