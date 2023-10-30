from django.contrib import admin
from django.contrib.auth.hashers import make_password

from app.models import *


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role')

    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 30
    ordering = ['id']
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.get_fields()]


admin.site.register(OperatingAccount, BaseAdmin)
admin.site.register(Product, BaseAdmin)
admin.site.register(Stock, BaseAdmin)
admin.site.register(Supplier, BaseAdmin)
admin.site.register(LiveBroadcast, BaseAdmin)
admin.site.register(LiveBroadcastPlan, BaseAdmin)
admin.site.register(LiveBroadcastInfo, BaseAdmin)
admin.site.register(Sales, BaseAdmin)
admin.site.register(PurchaseOrder, BaseAdmin)
admin.site.register(AfterSales, BaseAdmin)


admin.site.site_header = '直播管理系统后台'
admin.site.site_title = '直播管理系统后台'
admin.site.index_title = '直播管理系统后台'