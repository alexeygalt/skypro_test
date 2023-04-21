from django.contrib import admin, messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from network import models


@admin.register(models.Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ("title", "created")
    list_display_links = ("title",)
    search_fields = ("contact__city",)


@admin.register(models.RetailsNet)
@admin.register(models.IndiPred)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "indebtedness", "vendor")
    list_display_links = ("title",)
    search_fields = ("contact__city",)
    actions = ("debt_deletion",)

    def vendor(self, obj):
        ct = None
        if hasattr(obj, "factory") and obj.factory:
            ct = obj.factory
        elif hasattr(obj, "retails_net") and obj.retails_net:
            ct = obj.retails_net
        elif hasattr(obj, "indi_pred") and obj.indi_pred:
            ct = obj.indi_pred

        url = reverse(f'admin:{ct._meta.app_label}_{ct._meta.model_name}_change', args=(ct.id,))
        return mark_safe(f'<a href="%s">%s</a>' % (url, ct.title))

    @admin.action(description="Удаление задолжности")
    def debt_deletion(self, request, queryset):
        updates = queryset.update(indebtedness=0.00)
        self.message_user(request, ngettext("%d задолжность удалена",
                                            "%d задолности удалены", updates) % updates, messages.SUCCESS)


admin.site.register(models.Product)
admin.site.register(models.Contact)
