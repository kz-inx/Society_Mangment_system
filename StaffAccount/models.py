"""Importing the libraries are need in the system..."""
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

""" Create the custom manager for use in different in the fields """
class StaffManager(BaseUserManager):
    def create_staff(self, email, name, role, password=None):
        """
        Creates and saves a User with the given email, name,role and password.
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

""" Creating the database of the role mode in the our system """
class RolesStaff(models.Model):
    rolename = models.CharField(max_length=50, unique=True)

""" Creating the database of the staff-account in the our system """
class StaffAccount(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=30)
    role = models.ForeignKey(RolesStaff, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    is_change = models.BooleanField(default=False)

    objects = StaffManager()


