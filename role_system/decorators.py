# decorators.py

from functools import wraps
from django.http import HttpResponseForbidden
from role_permission import models
def check_permission(permission):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            # Check if the user has the required role
            if request.user.is_authenticated:
                code_names = models.RolePermission.objects.filter(role_id = request.user.role.id).values("permission__codename")
                print(permission,code_names)
                permitted = False
                for i in code_names:
                    if i["permission__codename"] == permission:
                        permitted = True
                if permitted:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("You don't have permission to access this page.")
        return wrapped_view
    return decorator
