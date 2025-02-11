from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, name, register_no, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('Password need to be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, register_no=register_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, name, register_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, register_no, password, **extra_fields)




class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    register_no = models.CharField(max_length=255)
    password =models.CharField(max_length = 100)
    is_staff = models.BooleanField(null=True)
    is_superuser = models.BooleanField(null=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role'] 