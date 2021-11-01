from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def _create_user(self, email, username, password=None, **extra_fields):
        """Check if user have set required fields"""
        if not email:
            raise ValueError("User must have email")
        if not username:
            raise ValueError("User must have username")
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        self._create_user(email=email, username=username, password=password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        user = self._create_user(email=email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('son', 'Son'),
        ('brother', 'Brother'),
        ('grandson', 'Grandson'),
        ('daughter', 'Daughter'),
        ('sister', 'Sister'),
        ('granddaughter', 'Granddaughter'),
        ('father', 'Father'),
        ('husband', 'Husband'),
        ('mother', 'Mother'),
        ('wife', 'Wife'),
        ('bride', 'Bride'),
        ('grandfather', 'Grandfather'),
        ('grandmother', 'Grandmother'),
    ]
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    family = models.ForeignKey('Family', on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(choices=ROLES, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True, null=True, blank=True) # can't be blank
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        return self.is_superuser


class Role(models.Model):
    ROLES = [
        ('son', 'Son'),
        ('brother', 'Brother'),
        ('grandson', 'Grandson'),
        ('daughter', 'Daughter'),
        ('sister', 'Sister'),
        ('granddaughter', 'Granddaughter'),
        ('father', 'Father'),
        ('husband', 'Husband'),
        ('mother', 'Mother'),
        ('wife', 'Wife'),
        ('bride', 'Bride'),
        ('grandpa', 'Grandpa'),
        ('grandma', 'Grandma'),
    ]
    role = models.CharField(max_length=255, unique=True, choices=ROLES)

    class Meta:
        verbose_name_plural = 'roles'
        db_table = 'roles'

    def __str__(self):
        return self.role


class UserRole(models.Model):
    """
    A class that stores user ids and role ids
    """
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    # user_id, filter by family and list the members,
    # and get the role for each of them

    def __str__(self):
        return f'{self.user2} - {self.role}'


class Family(models.Model):
    family_name = models.CharField(max_length=255)

    def __str__(self):
        return self.family_name

    class Meta:
        verbose_name_plural = 'families'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')

    def __str__(self):
        return self.user.first_name
