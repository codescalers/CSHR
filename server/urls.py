"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("auth/", include("server.cshr.routs.auth")),
                path("users/", include("server.cshr.routs.users")),
                path(
                    "training_courses/", include("server.cshr.routs.training_courses")
                ),
                path("myprofile/", include("server.cshr.routs.myinfo")),
                path("meeting/", include("server.cshr.routs.meetings")),
                path("event/", include("server.cshr.routs.event")),
                path("notifications/", include("server.cshr.routs.notifications")),
                path("home/", include("server.cshr.routs.landing_page")),
                path("compensation/", include("server.cshr.routs.compensation")),
                path("hrletter/", include("server.cshr.routs.hr_letters")),
                path("vacations/", include("server.cshr.routs.vacations")),
                path(
                    "company_properties/",
                    include("server.cshr.routs.company_properties"),
                ),

            ]
        ),
    ),
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Api Documentation",
            default_version="v1",
        ),
        public=False,
    )

    urlpatterns = (
        [
            # URLs specific only to django-debug-toolbar:
            path("__debug__/", include(debug_toolbar.urls)),
            # Swagger
            path(
                "swagger/",
                schema_view.with_ui("swagger", cache_timeout=0),
                name="schema-swagger-ui",
            ),
            path(
                "redoc/",
                schema_view.with_ui("redoc", cache_timeout=0),
                name="schema-redoc",
            ),
            # noqa: DJ05
        ]
        + urlpatterns
        + static(  # type: ignore
            # Serving media files in development only:
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
    )
