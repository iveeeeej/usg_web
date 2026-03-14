from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    def create_user(self, student_id, email, password=None, **extra_fields):
        if not student_id:
            raise ValueError("Users must have a student ID")

        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        user = self.model(
            student_id=student_id,
            email=email,
            **extra_fields
        )

        if not password:
            password = student_id

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'OFFICER')

        return self.create_user(student_id, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('OFFICER', 'Officer'),
        ('STUDENT', 'Student'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    position = models.CharField(max_length=100, null=True, blank=True)
    year_level = models.PositiveSmallIntegerField(null=True, blank=True)
    section = models.CharField(max_length=50, null=True, blank=True)
    course = models.CharField(max_length=150, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        name_parts = [self.first_name, self.middle_name, self.last_name]
        full_name = " ".join(part for part in name_parts if part)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return f"{self.student_id} - {self.get_full_name()}"
