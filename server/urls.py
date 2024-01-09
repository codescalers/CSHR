from django.contrib import admin
from django.urls import path, include
from server import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("auth/", include("server.cshr.routes.auth")),
                path("office/", include("server.cshr.routes.office")),
                path(
                    "evaluation/",
                    include("server.cshr.routes.evaluation"),
                ),
                path("users/", include("server.cshr.routes.users")),
                path(
                    "training_courses/", include("server.cshr.routes.training_courses")
                ),
                path("myprofile/", include("server.cshr.routes.myinfo")),
                path("meeting/", include("server.cshr.routes.meetings")),
                path("event/", include("server.cshr.routes.event")),
                path("home/", include("server.cshr.routes.landing_page")),
                path("compensations/", include("server.cshr.routes.compensation")),
                path("hr_letters/", include("server.cshr.routes.hr_letters")),
                path("vacations/", include("server.cshr.routes.vacations")),
                path("requests/", include("server.cshr.routes.requests")),
                path(
                    "official_documents/",
                    include("server.cshr.routes.official_documents"),
                ),
                path(
                    "company_properties/",
                    include("server.cshr.routes.company_properties"),
                ),
                path("notifications/", include("server.cshr.routes.notifications")),
            ]
        ),
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)


if settings.DEBUG:
    import debug_toolbar
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Api Documentation",
            default_version="v1",
        ),
        public=False,
    )

    urlpatterns = [
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
    ] + urlpatterns
