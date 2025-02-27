from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class NewUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Не задано имя пользователя')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True,
                                verbose_name="Имя пользователя")
    password = models.CharField(verbose_name="Пароль")
    is_staff = models.BooleanField(default=False,
                                   verbose_name="Модератор")
    is_superuser = models.BooleanField(default=False,
                                       verbose_name="Админ")

    USERNAME_FIELD = 'username'

    objects = NewUserManager()



class Component(models.Model):
    title = models.CharField(max_length=200)
    shortDescription = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    imgSrc = models.CharField(max_length=100, null=True, blank=True)


class Assembly(models.Model):
    dateCreated = models.DateField(auto_now_add=True)
    status = models.CharField(default="draft")
    creator = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING,
                                related_name='userAccess')
    moder = models.ForeignKey(AuthUser, on_delete=models.DO_NOTHING,
                              related_name='moderAccess', null=True, blank=True)
    dateModerated = models.DateField(null=True, blank=True)
    dateSaved = models.DateField(null=True, blank=True)
    satelliteName = models.CharField(max_length=150, null=True, blank=True)
    flyDate = models.DateField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)


class MM(models.Model):
    component = models.ForeignKey(Component, on_delete=models.DO_NOTHING)
    idAssembly = models.ForeignKey(Assembly, on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=1)

    class Meta:
        unique_together = (('component', 'idAssembly'),)
