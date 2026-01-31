from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(VaultEntry)
class PasswordAdmin(admin.ModelAdmin):
    list_display=(
        "service_name",
        "login_identifier",
        "owner",
        "created_at"
    )
    search_fields=(
        "service_name",
        "login_identifier",
    )
    readonly_fields = (
        "encrypted_password",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)
    