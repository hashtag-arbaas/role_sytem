from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.RolePermission)
admin.site.register(models.Permission)

admin.site.register(models.Role)


