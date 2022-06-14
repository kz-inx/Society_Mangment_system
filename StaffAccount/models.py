from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class StaffManager(BaseUserManager):
    def create_staff(self, email, name, role, password=None):
        """
        Creates and saves a User with the given email, name,house_no and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        staff = self.model(
            email=self.normalize_email(email),
            name=name,
            role=role,
        )

        staff.set_password(password)
        staff.save(using=self._db)
        return staff


class StaffAccount(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    password = models.CharField(max_length=100)

    objects = StaffManager()

class RolesStaff(models.Model):
    rolename = models.CharField(max_length=50)
