from django.contrib import admin
from django.apps import apps

# Register your models here.


class VacationAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "modified_at"]


class RequestsAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "modified_at"]


def autoregister(*app_list: str) -> None:
    """
    register all database models in the admin dashboard.
    """
    for app in app_list:
        for model_name, model in apps.get_app_config(app).models.items():
            if "_" not in model_name:
                admin.site.register(model, globals().get(model.__name__ + "Admin"))


admin.site.site_header = "CSHR Administration Settings"
admin.site.site_title = "CSHR Administration Settings"

autoregister("cshr")
