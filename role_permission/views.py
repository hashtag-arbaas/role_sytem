from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RoleForm, PermissionForm, TaskForm
from django.http import JsonResponse
from .models import Role, Permission, RolePermission, Task
from django.views.decorators.csrf import csrf_exempt
from role_system.decorators import check_permission as cp
def home(request):

    return render(request, 'home/home.html')

def readme(request):

    return render(request, 'home/readme.html')

def role_list(request):
    roles = Role.objects.all().values('id', 'name')
    print(roles)
    for role in roles:
        role_permissions = RolePermission.objects.filter(role_id=role["id"]).values("role_id", "permission_id", "permission__name","permission__codename")
        print(role_permissions)
        role["permissions"] = role_permissions 
    return render(request, 'home/roles.html', {'roles': roles})

def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('roles')
    else:
        form = RoleForm()
    return render(request, 'home/create_role.html', {'form': form})

def permission_list(request):
    permissions = Permission.objects.all()
    return render(request, 'home/permissions.html', {'permissions': permissions})

def create_permission(request):
    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('permissions')
    else:
        form = PermissionForm()
    return render(request, 'home/create_permission.html', {'form': form})

@csrf_exempt
def add_permissions(request):
    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        permission_id = request.POST.get('permission_id')
        try:
            role = Role.objects.get(pk=role_id)
            permission = Permission.objects.get(pk=permission_id)
            # Check if the permission is already assigned to the role
            if RolePermission.objects.filter(role=role, permission=permission).exists():
                role_permissions = RolePermission.objects.fiter(role=role).values("permission__name","permission__id")
                permissions_details = [rp.permission for rp in role_permissions]
                return JsonResponse({'message': 'Permission already assigned to the role',"permissions":permissions_details})
            else:
                RolePermission.objects.create(role=role, permission=permission)
                role_permissions = RolePermission.objects.filter(role=role).values("permission__name","permission__id")

                return JsonResponse({'message': 'Permission assigned to role successfully',"permissions":list(role_permissions)})
        except Role.DoesNotExist:
            return JsonResponse({'message': 'Role not found',"permissions":[]})
        except Permission.DoesNotExist:
            return JsonResponse({'message': 'Permission not found',"permissions":[]})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def remove_permissions(request):
    if request.method == 'POST':
        role_id = request.POST.get('role_id')
        permission_id = request.POST.get('permission_id')
        try:
            role_permissions = RolePermission.objects.filter(role_id=role_id, permission_id = permission_id)
            role_permissions.delete()
            RolePermission.objects.filter(role_id=role_id, permission_id=permission_id)
            role_permissions = RolePermission.objects.filter(role=role_id).values("permission__name","permission__id")
            print(role_permissions)
            return JsonResponse({'message': 'Permission removed',"permissions":list(role_permissions)})
        except Role.DoesNotExist:
            return JsonResponse({'message': 'Role not found',"permissions":[]})
        except Permission.DoesNotExist:
            return JsonResponse({'message': 'Permission not found',"permissions":[]})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def fetch_permissions(request):
    if request.method == 'GET':
        role_id = request.GET.get('role_id')
        try:
            role = Role.objects.get(pk=role_id)
            # Get all permissions not assigned to the role
            unassigned_permissions = Permission.objects.exclude(rolepermission__role=role)
            permissions_list = [{'id': permission.id, 'name': permission.name} for permission in unassigned_permissions]
            return JsonResponse({'permissions': permissions_list})
        except Role.DoesNotExist:
            return JsonResponse({'permissions': []})
    return JsonResponse({'permissions': []})

@csrf_exempt
@cp("view_task")
def task_list(request, pk=None):
    if request.method == 'DELETE':
        task_id = pk
        print("task_id==",task_id)
        Task.objects.get(id = task_id).delete()
    tasks = Task.objects.all()
    return render(request, 'home/tasks.html', {'tasks': tasks})

@cp("add_task")
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'home/create_task.html', {'form': form})
