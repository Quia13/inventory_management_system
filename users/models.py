from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


# ROLE MODEL
class Role(models.Model):
    class Meta:
        db_table = 'tbl_roles'

    role_id = models.BigAutoField(primary_key=True)
    role_type = models.CharField(max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_type


# CUSTOM USER MANAGER
class CustomUserManager(BaseUserManager):

    def _create_user(
        self,
        username,
        email,
        first_name,
        last_name,
        password,
        **extra_fields
    ):

        if not username:
            raise ValueError("Username is required")

        if not email:
            raise ValueError("Email is required")

        if not first_name:
            raise ValueError("First name is required")

        if not last_name:
            raise ValueError("Last name is required")

        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self,
        username,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(
            username,
            email,
            first_name,
            last_name,
            password,
            **extra_fields
        )

    def create_superuser(
        self,
        username,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields
    ):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            username,
            email,
            first_name,
            last_name,
            password,
            **extra_fields
        )


# =========================
# USER MODEL
# =========================
class User(AbstractBaseUser, PermissionsMixin):

    user_id = models.BigAutoField(primary_key=True)

    username = models.CharField(max_length=255, unique=True)

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100)

    middle_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    last_name = models.CharField(max_length=100)

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    profile = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name'
    ]

    class Meta:
        db_table = 'tbl_users'

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"

        return f"{self.first_name} {self.last_name}"