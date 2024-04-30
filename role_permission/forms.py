from django import forms
from .models import Role, Permission, Task

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name']

class PermissionForm(forms.ModelForm):
    print("in Permission form")
    class Meta:
        model = Permission
        fields = ['name', 'codename']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name']