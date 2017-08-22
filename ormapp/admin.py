#coding:utf-8


from django.contrib import admin
from django.contrib.admin import AdminSite
from ormapp.models import *


admin.site.site_url='/ormindex/'
admin.site.site_header='ORM后台管理'

class RepQueueAdmin(admin.ModelAdmin):
    list_display = ['describe','src_ip','src_path','src_ssh_user','src_ssh_pwd','src_dbid',
                    'dbps_port','extract_port','tgt_ip','tgt_path','tgt_ssh_user','tgt_ssh_pwd',
                    'tgt_dbid','collect_port','add_user','src_script_path','tgt_script_path']
    def save_model(self, request, obj, form, change):
        print obj.__dict__
        obj.add_user = request.user.username
        obj.save()

    def get_queryset(self, request):
        qs=super(RepQueueAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(add_user=request.user)

    fieldsets = (
        (
          None,{
              'fields':('describe',)
          }
        ),
        ('源端：',
         {
             'fields':('src_ip','src_path','src_ssh_user','src_ssh_pwd','src_dbid','dbps_port','extract_port','src_script_path')
         }
        ),
        ('目标端：',
         {
             'fields': ('tgt_ip','tgt_path','tgt_ssh_user','tgt_ssh_pwd','tgt_dbid','collect_port','tgt_script_path')
         }
        ),
    )

admin.site.register(rep_queue,RepQueueAdmin)



admin.site.register(src_moni_info)