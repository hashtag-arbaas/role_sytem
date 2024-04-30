from django.contrib.auth.models import AbstractUser
from  role_permission.models import Role
from django.db import models

class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=1)
