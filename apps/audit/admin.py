from django.contrib import admin

from apps.audit.models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("ts_utc", "action", "actor", "object_type", "object_id", "ip")
    list_filter = ("action", "object_type", "ts_utc")
    search_fields = ("object_id", "object_type", "action", "ip", "actor__username")
    readonly_fields = (
        "id",
        "ts_utc",
        "actor",
        "ip",
        "action",
        "object_type",
        "object_id",
        "before",
        "after",
    )
    ordering = ("-ts_utc", "-id")
    date_hierarchy = "ts_utc"
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
