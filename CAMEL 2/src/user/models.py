from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CamelUserManager(BaseUserManager):
    """Manager model to create users for CAMEL via admin backend"""
    def create_user(self, identifier, first_name, last_name, student, lecturer, email, password=None):
        '''Method for creating users'''
        if(not(identifier and first_name and last_name)):
            raise ValueError('Users must enter id number, first and last names')

        user = self.model(
            identifier=identifier,
            first_name=first_name,
            last_name=last_name,
            is_an_student=student,
            is_an_lecturer=lecturer,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, first_name, last_name, email, password=None):
        '''Method for creating superusers (admins)'''
        user = self.create_user(
            identifier=identifier,
            first_name=first_name,
            last_name=last_name,
            student=False,
            lecturer=False,
            email=email,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class CamelUser(AbstractBaseUser):
    """Model for CAMEL User for Admin/Lecturer/Student"""
    identifier = models.CharField(max_length=40, primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_an_student = models.BooleanField(default=False)
    is_an_lecturer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CamelUserManager()

    def __str__(self):
        return self.identifier

    def get_full_name(self):
        return "{} : {} {}".format(self.identifier, self.first_name, self.last_name)

    def get_short_name(self):
        return self.identifier

    get_short_name.short_description = "User Identifier"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_student(self):
        return self.is_an_student

    @property
    def is_teacher(self):
        return self.is_an_lecturer

    @property
    def is_camel_staff(self):
        return (self.is_an_lecturer or self.is_staff)
