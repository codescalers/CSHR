from django.contrib import admin
from django.urls import path, include
import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("auth/", include("cshr.routes.auth")),
                path("office/", include("cshr.routes.office")),
                path(
                    "evaluation/",
                    include("cshr.routes.evaluation"),
                ),
                path("users/", include("cshr.routes.users")),
                path("training_courses/", include("cshr.routes.training_courses")),
                path("myprofile/", include("cshr.routes.myinfo")),
                path("meeting/", include("cshr.routes.meetings")),
                path("event/", include("cshr.routes.event")),
                path("home/", include("cshr.routes.landing_page")),
                path("compensations/", include("cshr.routes.compensation")),
                path("hr_letters/", include("cshr.routes.hr_letters")),
                path("vacations/", include("cshr.routes.vacations")),
                path("requests/", include("cshr.routes.requests")),
                path(
                    "official_documents/",
                    include("cshr.routes.official_documents"),
                ),
                path(
                    "company_properties/",
                    include("cshr.routes.company_properties"),
                ),
                path("notifications/", include("cshr.routes.notifications")),
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
