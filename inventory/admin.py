from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Department, User, Device, Software, Licence, Maintenance, Credential, Documentation

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('type', 'brand', 'model', 'inv_number', 'assigned_to')

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('software', 'device', 'date_signing_contract', 'date_expire_contract')

class CredentialAdminForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = '__all__'

class CredentialAdmin(admin.ModelAdmin):
    form = CredentialAdminForm
    list_display = ("name", "hostname", "username", "masked_password", "last_changed")
    fields = (
        "name",
        "hostname",
        "username",
        "password",      # password uvijek ovdje
        "last_changed",
        "description",
    )
    readonly_fields = ("last_changed",)

    def masked_password(self, obj):
        return "******"
    masked_password.short_description = "Password"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            if 'password' in form.base_fields:
                form.base_fields['password'].widget = forms.TextInput()
        else:
            if 'password' in form.base_fields:
                form.base_fields['password'].widget = forms.PasswordInput(render_value=True)
                form.base_fields['password'].disabled = True  # učini polje readonly
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser and 'password' not in readonly:
            readonly.append('password')
        return readonly

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ("title", "doc_type", "related_device", "related_software", "short_description", "created_at", "view_document")
    search_fields = ("title", "related_device__brand", "related_software__name")
    list_filter = ("doc_type", "created_at", "related_device", "related_software")
    readonly_fields = ("created_at",)

    def short_description(self, obj):
        return (obj.description[:40] + "...") if obj.description and len(obj.description) > 40 else obj.description
    short_description.short_description = "Opis"

    def view_document(self, obj):
        if obj.upload:
            return format_html('<a href="{}" target="_blank">Otvori</a>', obj.upload.url)
        return "-"
    view_document.short_description = "Dokument"

admin.site.register(Credential, CredentialAdmin)
admin.site.register(Department)
admin.site.register(User)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Software)
admin.site.register(Licence)
admin.site.register(Maintenance, MaintenanceAdmin)
