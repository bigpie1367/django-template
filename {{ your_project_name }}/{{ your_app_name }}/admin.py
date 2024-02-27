from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import Department, Grade

User = get_user_model()


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("identifier", "display_name", "department_email")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("identifier", "display_name",)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "fullname",
                    "email",
                    "birth",
                    "phone"
                )
            }
        ),
        (
            _("Office Info"),
            {
                "fields": (
                    "department",
                    "grade"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = ["username", "fullname", "department",
                    "grade", "is_active", "is_superuser"]
    list_filter = ["department", "grade"]
    search_fields = ["fullname"]
